import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t1")

lc = 1e-2
# down surf
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(.1, .1, 0, lc, 3)
gmsh.model.geo.addPoint(0, .1, 0, lc, 4)
# upper surf
gmsh.model.geo.addPoint(0, 0, 0.1, lc, 5)
gmsh.model.geo.addPoint(.1, 0, 0.1, lc, 6)
gmsh.model.geo.addPoint(.1, .1, 0.1, lc, 7)
gmsh.model.geo.addPoint(0, .1, 0.1, lc, 8)

# top 
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)
# bottom
gmsh.model.geo.addLine(5, 6, 5)
gmsh.model.geo.addLine(6, 7, 6)
gmsh.model.geo.addLine(7, 8, 7)
gmsh.model.geo.addLine(8, 5, 8)
# sides
gmsh.model.geo.addLine(1, 5, 9)
gmsh.model.geo.addLine(2, 6, 10)
gmsh.model.geo.addLine(3, 7, 11)
gmsh.model.geo.addLine(4, 8, 12)

#1
gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
gmsh.model.geo.addPlaneSurface([1], 1)
#2
gmsh.model.geo.addCurveLoop([5, 6, 7, 8], 2)
gmsh.model.geo.addPlaneSurface([2], 2)
#3
gmsh.model.geo.addCurveLoop([1, 10, -5, -9], 3)
gmsh.model.geo.addPlaneSurface([3], 3)
#4
gmsh.model.geo.addCurveLoop([2, 11, -6, -10], 4)
gmsh.model.geo.addPlaneSurface([4], 4)
#5
gmsh.model.geo.addCurveLoop([3, 12, -7, -11], 5)
gmsh.model.geo.addPlaneSurface([5], 5)
#6
gmsh.model.geo.addCurveLoop([4, 9, -8, -12], 6)
gmsh.model.geo.addPlaneSurface([6], 6)


l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(6)])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("t1.msh")
#gmsh.write("t1.geo_unrolled")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()