from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import splipy as spl
import splipy.surface_factory as spf
from mpl_toolkits.mplot3d import Axes3D
################################################################################

def Area_Plot():

    with G2('Area.g2') as my_file:
        my_area = my_file.read()

    n = 250  # number of evaluation points
    area = my_area[0]   # create the NURBS curve
    u = np.linspace(area.start('u'), area.end('u'), n)  # parametric evaluation points
    v = np.linspace(area.start('v'), area.end('v'), n)
    x = area(u,v)  # physical (x,y)-coordinates, size (n,2)

    fig = plt.figure()
    plt.plot(x[:,:,0],x[:,:,1],'k-')
    plt.plot(x[:,:,0].T,x[:,:,1].T,'k-')
    plt.legend('NURBS Area')
    plt.show()


if __name__ == "__main__":
    Area_Plot()
