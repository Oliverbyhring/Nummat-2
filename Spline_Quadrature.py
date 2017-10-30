################################################################################
import time
import numpy as np
import scipy as sp
import splipy as sp
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)

################################################################################

TOLERANCE = 1e-11

#kontrollert og funnet ok dato:
def Prepare_Data(T, p): # T is knot vector, p is degree of polynomial
    # 0) Prepare knot vector
    if (len(T) - p - 1) % 2: # n=len(T)-p-1. We add a knot in the knot vector if n is not even
        new_T = T[:p+1]
        new_T.append((T[p] + T[p+1])/2)
        new_T += T[p+1:]
        T = new_T
    n = int((len(T) - p - 1) / 2)
    print("2n =", 2*n)

    # 1) Calculate exact integrals
    integrals_c = np.zeros(2*n)
    for i in range(2*n):
        integrals_c[i] = (T[i+p+1] - T[i])/(p+1)
    integrals_c = integrals_c.T #Trenger vi å transpose denne?
    print(integrals_c)
    print("Ser faen meg legit ut. De basisfunksjonene som er helt inneholdt i intervallet integreres til 1, de mot kantene har deler som 'ligger utenfor'")

    # 2) Generate initial xi and initial w
    # The initial guess of xi_i must have length n and be somehow distributed over the intervall. Using Greville.
    xi = np.zeros(n)
    tau_abscissa = np.zeros(n)
    # Neste her skal være 2n!!!!!!!!!!!!!!!!!!!!!!
    for i in range(n): # Skjønner ikke hvordan vi skal få 2n av disse!!!!!!!!!!!!!!!!!!!!!!
        tau_abscissa[i] = sum(T[i:i+p])/p #Tau er 1-indeksert i "Optimal Quadrature", 0-indeksert her.
    for i in range(n):
        xi[i] = (tau_abscissa[i] + tau_abscissa[i])/2 #Skal være den uinder!!!!!!!!!!!!!!!!!!!!!!
        # xi[i] = (tau_abscissa[2 * i] + tau_abscissa[2 * i + 1]) / 2
    print(xi)

    w = np.zeros(n) # Denne initialiseres som fra optimal quad-boka
    for i in range(n):
        w[i] = integrals_c[2*i] + integrals_c[2*i+1]

    # 3) Generate basis functions, evaluer og finn partiellderiverte av F
    basis = sp.BSplineBasis(order=p+1, knots=T)
    print("basis", basis)
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

    # 4) Beregne F0(z)
    F = 

    # 5) Sette sammen en Jacobi med redusert bandwidth
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
    inv_jacobi = np.linalg.inv(jacobian) #Jacobian er singular hurra!
    print(inv_jacobi)

    return T, n, integrals_c, F, inv_jacobi

def Assembly(basis,I,W,X,n):
    return 0

def Spline_Quadrature():
    T = [0, 0, 0, 1, 2, 3, 4, 4, 4]
    p = 2
    T, n, integrals_c = Prepare_Data(T, p)
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