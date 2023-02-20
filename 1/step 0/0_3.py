import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t3")

lc = 1e-2
#------------ bottom
gmsh.model.occ.addPoint(0, 0, 0, lc, 1)
gmsh.model.occ.addPoint(-0.1, 0, 0, lc, 2)
gmsh.model.occ.addPoint(0.1, 0, 0, lc, 3)

gmsh.model.occ.addCircleArc(2, 1, 3, 1)
gmsh.model.occ.addCircleArc(3, 1, 2, 2)

gmsh.model.occ.addCurveLoop([1, 2], 1)
gmsh.model.occ.addPlaneSurface([1], 1)

#------------ top
gmsh.model.occ.addPoint(0, 0, 0.2, lc, 4)
gmsh.model.occ.addPoint(-0.1, 0, 0.2, lc, 5)
gmsh.model.occ.addPoint(0.1, 0, 0.2, lc, 6)

gmsh.model.occ.addCircleArc(5, 4, 6, 3)
gmsh.model.occ.addCircleArc(6, 4, 5, 4)

gmsh.model.occ.addCurveLoop([3, 4], 2)
gmsh.model.occ.addPlaneSurface([2], 2)

gmsh.model.occ.addLine(2, 5, 5)
gmsh.model.occ.addLine(3, 6, 6)

gmsh.model.occ.addCurveLoop([1, 6, -3, -5], 3)
gmsh.model.occ.addBSplineFilling(3, 3)

gmsh.model.occ.addCurveLoop([2, 5, -4, 6], 5)
gmsh.model.occ.addBSplineFilling(5, 5)

l = gmsh.model.occ.addSurfaceLoop([1,2,3,5])
gmsh.model.occ.addVolume([l])


gmsh.model.occ.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("t3.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()