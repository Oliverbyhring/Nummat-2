################################################################################
import time
import numpy as np
import scipy as sp
import splipy as sp
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)

################################################################################

TOLERANCE = 1e-11

#kontrollert og funnet ok 30.10
def Prepare_Data(T, p): # T is knot vector, p is degree of polynomial
    # 1) Prepare knot vector
    if (len(T) - p - 1) % 2: # n=len(T)-p-1. We add a knot in the knot vector if n is not even
        new_T = T[:p+1]
        new_T.append((T[p] + T[p+1])/2)
        new_T += T[p+1:]
        T = new_T
    n = int((len(T) - p - 1) / 2)
    print("2n =", 2*n)

    # 2) Generate basis functions, initial xi and initial w
    basis = sp.BSplineBasis(order=p+1, knots=T)
    print("basis", basis)
    xi = np.linspace(0, 4, n) #This must be our initial guess of xi
    w = np.array([1,2,3]) # Denne initialiseres som fra optimal quad-boka

    B = np.array(basis.evaluate(xi)).transpose() # B.shape = (2n basis functions, n evaluation points)
    print("B\n", B)
    if B.shape != (2*n, n):
        print("Not 2nXn! Du har glemt a order=p+1!")
    dFdw = B  # dFdw is equal to B!
    print("dFdw\n", dFdw)
    B_der = np.array(basis.evaluate(xi, d=1)).transpose()
    print("B_der\n", B_der)
    dFdxi = B_der*w # Dette er ikke matrix multiplication, men elementwise vekting av kolonnene i B_der med elementene i w
    print("dFdxi\n", dFdxi)

    # 3) Sette sammen en Jacobi med redusert bandwidth
    naive_jacobi = np.concatenate((dFdw, dFdxi), axis=1)
    print("naive_jacobi\n", naive_jacobi)
    split_dFdw = np.hsplit(dFdw, n)
    print(split_dFdw)
    split_dFdxi = np.hsplit(dFdxi, n)
    print(split_dFdxi)
    jacobian = np.concatenate((split_dFdw[0], split_dFdxi[0]), axis=1)
    for i in range(1,n):
        jacobian = np.concatenate((jacobian, split_dFdw[i], split_dFdxi[i]), axis=1)
    print("jacobian\n", jacobian)
    print("But is the jacobian a numpy array now?")
    # Invert Jacobian
    inv_jacobi = np.linalg.inv(jacobian)
    print(inv_jacobi)
    

    # 4) Calculate exact integrals
    integrals_c = [0]

    return T, n, integrals_c

Prepare_Data([0,0,0,1,2,3,4,4,4], 2)

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