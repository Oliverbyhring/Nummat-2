from sys import path
path.append('Code Facilities') # hva betyr dette?
from splipy.IO import * # OI changed to io in last edit

# G2 files are native GoTools (http://www.sintef.no/projectweb/geometry-toolkits/gotools/)

# Read a single NURBS patch from the file 'sphere.g2'
with G2('Curve.g2') as my_file:
    my_sphere = my_file.read()
