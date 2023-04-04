import gmsh
import math
import os
import sys

gmsh.initialize()

# we are using stl file of a phrog (sciencific term)
path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, 'phrog.stl'))

n = gmsh.model.getDimension()
s = gmsh.model.getEntities(n)
l = gmsh.model.geo.addSurfaceLoop([s[i][1] for i in range(len(s))])

gmsh.model.geo.addVolume([l])
print("Volume added")

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

gmsh.write('t_frog.msh')

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()