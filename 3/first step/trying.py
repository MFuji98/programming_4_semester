from fenics import *
from mshr import *

T = 3            # final time
num_steps = 10000   # number of time steps
dt = T / num_steps # time step size
mu = 0.002         # dynamic viscosity
rho = 1            # density

# Create mesh
channel = Rectangle(Point(0, 0), Point(2.2, 0.41))
cube1 = Rectangle(Point(0.16, 0.14), Point(0.24, 0.20))
cube2 = Rectangle(Point(0.40, 0.18), Point(0.50, 0.34))
cube3 = Rectangle(Point(0.60, 0.08), Point(0.70, 0.15))
cube4 = Rectangle(Point(1.50, 0.13), Point(1.75, 0.30))
cube5 = Rectangle(Point(1.00, 0.13), Point(1.30, 0.20))
domain = channel - cube2 - cube1 - cube3 - cube4 - cube5
mesh = generate_mesh(domain, 66)

# Define function spaces
V = VectorFunctionSpace(mesh, 'P', 2)
Q = FunctionSpace(mesh, 'P', 1)

# Define boundaries
inflow   = 'near(x[0], 0)'
outflow  = 'near(x[0], 2.2)'
walls    = 'near(x[1], 0) || near(x[1], 0.41)'
cube1 = 'on_boundary && x[0]>0.1 && x[0]<0.3 && x[1]>0.1 && x[1]<0.3'
cube2 = 'on_boundary && x[0]>0.3 && x[0]<0.6 && x[1]>0.1 && x[1]<0.4'
cube3 = 'on_boundary && x[0]>0.5 && x[0]<0.8 && x[1]>0 && x[1]<0.2'
cube4 = 'on_boundary && x[0]>0.9 && x[0]<1.4 && x[1]>0.10 && x[1]<0.4'
cube5 = 'on_boundary && x[0]>1.60 && x[0]<1.80 && x[1]>0.10 && x[1]<0.3'

# Define inflow profile
inflow_profile = ('4.0*1.5*x[1]*(0.41 - x[1]) / pow(0.41, 2)', '0')

# Define boundary conditions
bcu_inflow = DirichletBC(V, Expression(inflow_profile, degree=2), inflow)
bcu_walls = DirichletBC(V, Constant((0, 0)), walls)
bcu_cube1 = DirichletBC(V, Constant((0, 0)), cube1)
bcu_cube2 = DirichletBC(V, Constant((0, 0)), cube2)
bcu_cube3 = DirichletBC(V, Constant((0, 0)), cube3)
bcu_cube4 = DirichletBC(V, Constant((0, 0)), cube4)
bcu_cube5 = DirichletBC(V, Constant((0, 0)), cube5)

bcp_outflow = DirichletBC(Q, Constant(0), outflow)
bcu = [bcu_inflow, bcu_walls, bcu_cube1, bcu_cube2, bcu_cube3, bcu_cube4, bcu_cube5]
bcp = [bcp_outflow]

# Define trial and test functions
u = TrialFunction(V)
v = TestFunction(V)
p = TrialFunction(Q)
q = TestFunction(Q)

# Define functions for solutions at previous and current time steps
u_n = Function(V)
u_  = Function(V)
p_n = Function(Q)
p_  = Function(Q)

# Define expressions used in variational forms
U  = 0.5*(u_n + u)
n  = FacetNormal(mesh)
f  = Constant((0, 0))
k  = Constant(dt)
mu = Constant(mu)
rho = Constant(rho)

# Define symmetric gradient
def epsilon(u):
    return sym(nabla_grad(u))

# Define stress tensor
def sigma(u, p):
    return 2*mu*epsilon(u) - p*Identity(len(u))

# Define variational problem for step 1
F1 = rho*dot((u - u_n) / k, v)*dx \
   + rho*dot(dot(u_n, nabla_grad(u_n)), v)*dx \
   + inner(sigma(U, p_n), epsilon(v))*dx \
   + dot(p_n*n, v)*ds - dot(mu*nabla_grad(U)*n, v)*ds \
   - dot(f, v)*dx
a1 = lhs(F1)
L1 = rhs(F1)

# Define variational problem for step 2
a2 = dot(nabla_grad(p), nabla_grad(q))*dx
L2 = dot(nabla_grad(p_n), nabla_grad(q))*dx - (1/k)*div(u_)*q*dx

# Define variational problem for step 3
a3 = dot(u, v)*dx
L3 = dot(u_, v)*dx - k*dot(nabla_grad(p_ - p_n), v)*dx

# Assemble matrices
A1 = assemble(a1)
A2 = assemble(a2)
A3 = assemble(a3)

# Apply boundary conditions to matrices
[bc.apply(A1) for bc in bcu]
[bc.apply(A2) for bc in bcp]

# VTK files for visualization
file_u = File('navier_stokes_cylinder/velocity.pvd')
file_p = File('navier_stokes_cylinder/pressure.pvd')

# Time-stepping
t = 0
for n in range(num_steps):

    # Update current time
    t += dt

    # Step 1: Tentative velocity step
    b1 = assemble(L1)
    [bc.apply(b1) for bc in bcu]
    solve(A1, u_.vector(), b1, 'bicgstab', 'petsc_amg')

    # Step 2: Pressure correction step
    b2 = assemble(L2)
    [bc.apply(b2) for bc in bcp]
    solve(A2, p_.vector(), b2, 'bicgstab', 'petsc_amg')

    # Step 3: Velocity correction step
    b3 = assemble(L3)
    solve(A3, u_.vector(), b3, 'cg', 'sor')

    # Save solution to file (XDMF/HDF5)
    file_u << u_
    file_p << p_

    # Update previous solution
    u_n.assign(u_)
    p_n.assign(p_)

    print("Current time: %f / %f" % (t, T))








