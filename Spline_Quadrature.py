################################################################################
import numpy as np
import scipy as sp
import splipy as sp
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)

################################################################################

TOLERANCE = 1e-11

#kontrollert og funnet ok 30.10
def Prepare_Data(T, p): # T is knot vector, p is degree of polynomial
    # 1) Prepare knot vector
    if len(T)%2: #if odd number of knots, we add a knot
        new_T = T[:p+1]
        new_T.append((T[p] + T[p+1])/2)
        new_T += T[p+1:]
        T = new_T

    # For å ha n basisfunksjoner må knot vector T ha n+p+1 elementer!
    n = int((len(T) - p - 1)/2)
    print("Jevnt antall basisfunksjoner, 2n =", 2*n)
    if abs((len(T) - p - 1) % 2) > 1e-10:
        print("n er ikke heltall!")
        return

    # 2) Generate basis functions, initial xi and initial w
    basis = sp.BSplineBasis(order=p, knots=T)
    print(basis)
    xi = np.linspace(0, 4, n) #This must be our initial guess of xi
    w = np.ones(n)

    B = np.array(basis.evaluate(xi))  # B.shape = (n evaluation points, 2n basis functions)
    B = B.transpose() # B.shape = (2n basis functions, n evaluation points)
    print(B)
    if B.shape != (2*n, n):
        print("Not 2nXn!")
        return
    dFdw = B  # dFdw is equal to B!

    #dFdxi =

    # 3) Calculate exact integrals
    integrals_c = [0]

    return T, n, integrals_c

Prepare_Data([0,0,0,1,2,3,4,4,4], 3)

def Assembly(basis,I,W,X,n):
    return 0

def Spline_Quadrature():
    knots = [0, 0, 0, 1, 2, 3, 4, 4, 4]
"""
    Jacobian = Assembly()
    xk = x0
    counter = 0
    while np.linalg.norm(F(xk), ord=np.inf) > TOLERANCE:
        Assembly()
        dx = Jacobian * F
        xk = xk - dx
        counter += 1
    print(counter, 'iterations')

    return xk
"""

if __name__ == "__main__":
    Spline_Quadrature()