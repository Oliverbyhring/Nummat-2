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
    v = curve.derivative(t, 1)  # velocity at all points
    a = curve.derivative(t, 2)  # acceleration at all points


    # plot the curve.  {and get reference to the acceleration/velocity lines which we
    # will update during animation} OMITTED

    fig = plt.figure()
    plt.plot(x[:, 0], x[:, 1], 'k-')
    #velocity, = plt.plot([x[0, 0], x[0, 0] + v[0, 0]], [x[0, 1], x[0, 1] + v[0, 1]], 'r-', linewidth=2)
    #acceleration, = plt.plot([x[0, 0], x[0, 0] + a[0, 0]], [x[0, 1], x[0, 1] + a[0, 1]], 'b-', linewidth=3)
    #plt.axis('equal')
    plt.legend('NURBS Curve')
    plt.show()

if __name__ == "__main__":
    Curve_Plot()
