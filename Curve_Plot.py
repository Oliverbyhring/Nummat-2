from splipy.IO import * # OI changed to io in last edit
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Read a single NURBS patch from the file 'sphere.g2'
with G2('Curve.g2') as my_file:
    my_curve = my_file.read()


n = 250  # number of evaluation points
curve = my_curve[0]   # create the NURBS#  curve
t = np.linspace(curve.start(0), curve.end(0), n)  # parametric evaluation points
x = curve(t)  # physical (x,y)-coordinates, size (n,2)
v = curve.derivative(t, 1)  # velocity at all points
a = curve.derivative(t, 2)  # acceleration at all points

# plot the curve.  OMITTED: {and get reference to the acceleration/velocity lines which we
# will update during animation}
fig = plt.figure()
plt.plot(x[:, 0], x[:, 1], 'k-')
#velocity, = plt.plot([x[0, 0], x[0, 0] + v[0, 0]], [x[0, 1], x[0, 1] + v[0, 1]], 'r-', linewidth=2)
#acceleration, = plt.plot([x[0, 0], x[0, 0] + a[0, 0]], [x[0, 1], x[0, 1] + a[0, 1]], 'b-', linewidth=3)
#plt.axis('equal')
plt.legend(('NURBS Curve', 'Velocity - bla', 'Acceleration -bla'))

plt.show()
