from splipy.IO import * # "OI" changed to "io" in last edit - I dont have last edit
import matplotlib.pyplot as plt
import numpy as np
import Spline_Quadrature as sq
# Read a single NURBS patch from the file 'Curve.g2' NB: this file must be in the same directory

with G2('Curve.g2') as my_file:
    my_curve = my_file.read()

curve = my_curve[0]   # create the NURBS curve
w, ksi = sq.Spline_Quadrature(curve.knots(),curve.order())


print(w,ksi)
