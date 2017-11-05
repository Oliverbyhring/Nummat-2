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
    t = np.linspace(area.start(0), area.end(0), n)  # parametric evaluation points
    x = area(t)  # physical (x,y)-coordinates, size (n,2)

    fig = plt.figure()
    Axes3D.plot_surface(x[:, 0,0],x[:, 0,1])
    plt.legend('NURBS Curve')
    plt.show()


if __name__ == "__main__":
    Area_Plot()
