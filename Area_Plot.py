from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import splipy as spl
import splipy.surface_factory as spf
from mpl_toolkits.mplot3d import Axes3D
################################################################################

def Area_Plot():

    with G2('Area.g2') as my_file:
        my_surface = my_file.read()

    n = 250  # number of evaluation points
    surface = my_surface[0]   # create the NURBS surface
    u = np.linspace(surface.start('u'), surface.end('u'), n)  # parametric evaluation points
    v = np.linspace(surface.start('v'), surface.end('v'), n)
    x = surface(u,v)  # physical (x,y)-coordinates, size (n,2)

    fig = plt.figure()
    plt.plot(x[:,:,0],   x[:,:,1],   'k-')
    plt.plot(x[:,:,0].T, x[:,:,1].T, 'k-')
    plt.legend('NURBS Area')
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    Area_Plot()
