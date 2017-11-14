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

    # Get the surface object from my_Area

    surface = my_Area[0]   # create the NURBS surface
    T = surface.knots(0, True) # get knots from tuple object
    p = surface.order(0) - 1 # get degree (order - 1) from tuble object


    # Compute the weights and nodes from the knot vector with order p

    w, ksi = sq.Spline_Quadrature(T,p)

    # Evaluate the surface at the nodes to obtain du, dv

    derivative = surface.derivative(ksi)
    du = derivative[:,0]
    dv = derivative[:,1]

    # Compute the surface integral using the J(du,dv) and the computed weights

    A = 0 # surface integral
    for i in range(len(ksi)):
        A += w[i]*np.cross(du[i],dv[i])

    return A


if __name__ == "__main__":
    print(Area_Integral())
