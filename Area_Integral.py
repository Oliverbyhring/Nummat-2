from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import Spline_Quadrature as sq
#import splipy as spl
#import scipy as sp
#import sys

def Area_Integral():
    # Read a single NURBS patch from the file 'Curve.g2' NB: this file must be in the same directory

    with G2('Area.g2') as my_file:
        my_Area = my_file.read()

    surface = my_Area[0]   # create the NURBS surface
    T = surface.knots(0, True) # få ut skjøtene fra tuple-objekt
    p = surface.order(0) - 1 # få ut ordenen fra tuple-objekt

    w, ksi = sq.Spline_Quadrature(T,p)

    derivative = surface.derivative(ksi)
    du = derivative[:,0]
    dv = derivative[:,1]

    A = 0 # surface integral
    for i in range(len(ksi)):
        A += w[i]*np.cross(du[i],dv[i])
    print(A)
    return A


if __name__ == "__main__":
    Area_Integral()
