#from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import splipy as spl
from splipy.IO import *
import sys
################################################################################


def Curve_Plot():

    # Read a single NURBS patch from the file 'Curve.g2' NB: this file must be in the same directory

    with G2('Curve.g2') as my_file:
        my_curve = my_file.read()


    n = 250  # number of evaluation points
    curve = my_curve[0]   # create the NURBS curve
    t = np.linspace(curve.start(0), curve.end(0), n)  # parametric evaluation points
    x = curve(t)  # physical (x,y)-coordinates, size (n,2)


    # plot the curve.  
    fig = plt.figure()
    plt.plot(x[:, 0], x[:, 1], 'k-')
    plt.legend('NURBS Curve')
    plt.show()

if __name__ == "__main__":
    Curve_Plot()
