from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import Spline_Quadrature as sq
#import splipy as spl
#import scipy as sp
#import sys

def Curve_Integral():
    # Read a single NURBS patch from the file 'Curve.g2' NB: this file must be in the same directory

    with G2('Curve.g2') as my_file:
        my_curve = my_file.read()

    curve = my_curve[0]   # create the NURBS curve
    T = curve.knots()[0] # få ut lista fra tuple-objekt
    p = curve.order()[0] # få ut ordenen fra tuple-objekt

    w, ksi = sq.Spline_Quadrature(T,p)
    #
    # I = 0 # line integral
    # for i in range(len(ksi)):
    #     I += w[i]*curve(ksi[i])*abs(curve.derivative(ksi[i]))
    # return I


if __name__ == "__main__":
    Curve_Integral()
