from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import splipy as spl
import scipy as sp
import sys
import Spline_Quadrature as sq

def Area_Integral():

    # Read surface file and store

    with G2('Area.g2') as my_file:
        my_Area = my_file.read()

    # Get the surface object, and fetch two knot vectors / two degrees

    surface = my_Area[0]   # create the NURBS surface
    T1 = surface.knots(0, True) # get knots from tuple object
    T2 = surface.knots(1, True)
    p1 = surface.order(0) - 1 # get degree (order - 1) from tuble object
    p2 = surface.order(1) - 1

    # Compute two sets of weights and nodes (2D-surface)

    w1, ksi1 = sq.Spline_Quadrature(T1,p1)
    w2, ksi2 = sq.Spline_Quadrature(T2,p2)

    # Compute the surface integral using the |J(du,dv)| and the computed weights

    A = 0 # surface integral

    for i in range(len(ksi1)):
        for j in range(len(ksi2)):
            du = surface.derivative(ksi1[i],ksi2[j],d=(1,0))
            dv = surface.derivative(ksi1[i],ksi2[j],d=(0,1))
            A += w1[i] * w2[j] * abs(np.cross(du,dv))

    return A


if __name__ == "__main__":
    print(Area_Integral())
