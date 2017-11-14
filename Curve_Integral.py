from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import splipy as spl
import scipy as sp
import sys
import Spline_Quadrature as sq

def Curve_Integral():

    # Read a single NURBS patch from the file 'Curve.g2'

    with G2('Curve.g2') as my_file:
        my_curve = my_file.read()

    # Create the NURBS curve, and get knot vector and order from curve object

    curve = my_curve[0]
    T = curve.knots(0, True)
    p = curve.order(0) - 1 # degree = order - 1

    # Compute the weights and nodes from the objects knot vector and degree

    w, ksi = sq.Spline_Quadrature(T,p)

    I = 0 # line integral
    E = np.zeros(len(ksi))


    # Compute the line integral: each step is weight * (du^2+dv^2) ^ 0.5

    for i in range(len(ksi)):
        E = curve.derivative(ksi[i]) # evaluate the derivative in node i
        I += w[i]*np.sqrt(E[0]**2+E[1]**2)


    return I


if __name__ == "__main__":
    print(Curve_Integral())
