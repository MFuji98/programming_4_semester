import gmsh
import math
import os
import sys

gmsh.initialize()

# Let's merge an STL mesh that we would like to remesh (from the parent
# directory):
path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, 'torrus.stl'))

gmsh.initialize()
#gmsh.option.setNumber("General.Terminal", 1)
gmsh.option.setNumber("Mesh.Algorithm", 3);
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.2);
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.5);
gmsh.option.setNumber("Mesh.Optimize",1)
gmsh.option.setNumber("Mesh.QualityType",2);

n = gmsh.model.getDimension()
s = gmsh.model.getEntities(n)
l = gmsh.model.geo.addSurfaceLoop([s[i][1] for i in range(len(s))])

gmsh.model.geo.addVolume([l])
print("Volume added")
gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write('toroid.msh')

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()