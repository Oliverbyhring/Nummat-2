################################################################################
import time
import numpy as np
import scipy as sp
import splipy as spl
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)

################################################################################

TOLERANCE = 1e-11

# Sist oppdatert 02.11.17
def Prepare_Data(T, p): # T is knot vector, p is degree of polynomial
    # 0) Prepare knot vector
    if (len(T) - p - 1) % 2: # n=len(T)-p-1. We add a knot in the knot vector if n is not even
        new_T = T[:p+1]
        new_T.append((T[p] + T[p+1])/2)
        new_T += T[p+1:]
        T = new_T
    print("T =", T)
    n = int((len(T) - p - 1) / 2)
    print("2n =", 2*n)

    # 1) Calculate exact integrals
    integrals_c = np.zeros(2*n)
    for i in range(2*n):
        integrals_c[i] = (T[i+p+1] - T[i])/(p+1)
    print("integrals_c", integrals_c)
    # Ser bra ut. De basisfunksjonene som er helt inneholdt i intervallet integreres til 1, de mot kantene har deler som 'ligger utenfor'

    # 2) Generate initial xi and w
    xi = np.zeros(n)
    tau_abscissa = np.zeros(2*n)
    for i in range(2*n):
        tau_abscissa[i] = sum(T[i+1:i+p+1])/p
    for i in range(n):
        xi[i] = (tau_abscissa[2 * i] + tau_abscissa[2 * i + 1]) / 2
    print("xi", xi)

    w = np.zeros(n)
    for i in range(n):
        w[i] = integrals_c[2*i] + integrals_c[2*i+1]
    print("w", w)

    # 3) Generate basis functions, evaluer og finn partiellderiverte av F
    basis = spl.BSplineBasis(order=p + 1, knots=T)
    print("basis", basis)
    return basis, integrals_c, w, xi, n

# Sist oppdatert 02.11.17
def Assembly(basis, integrals_c, w, xi, n):
    # 1) Lag en N-matrise med basisfunksjonene N evaluert i xi-punktene
    N = np.array(basis.evaluate(xi)) # N.shape = (n evaluation points, 2n basis functions)
    # Vi venter med å transponere siden det gjør det lettere å flette sammen en jacobian

    # 2) Beregn Fn
    Fn = N.transpose().dot(w) - integrals_c
    # print("Fn", Fn)

    # 3) Beregn Jacobien med redusert bandwidth og sparse. dFdw tilsvarer N, dFdxi[i][j] tilsvarer w[i]*N[j]'(xi[i]).
    J = np.zeros((2*n, 2*n))
    dFdxi = np.array(basis.evaluate(xi, d=1)).transpose()*w # Elementwise vekting av kolonnene i N'(xi) med element i w
    dFdxi = dFdxi.transpose() # Gir dobbel transponering merkbart lengre kjøretid????
    for i in range(n):
        J[2*i] = N[i] # dF/dw tilsvarer N
        J[2*i+1] = dFdxi[i]
    J = J.transpose()
    # print("J", J)

    return Fn, J

def Spline_Quadrature():
    T = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6]
    p = 3 # Antall repeterende elemter i T, minus 1
    basis, integrals_c, w, xi, n = Prepare_Data(T, p) # T er endret men brukes ikke videre i koden så returneres ikke

    dz = np.array([10000])
    counter = 0
    print("\nBegynner iterasjon")
    while abs(np.linalg.norm(dz, ord=np.inf)) > TOLERANCE and counter < 500:
        Fn, J = Assembly(basis, integrals_c, w, xi, n)
        dz = sp.linalg.solve(J, Fn) # dz er på formen [ w_1 xi_1 x_2 xi_2 ... ]
        for i in range(n):
            w[i] -= dz[2*i]
            xi[i] -= dz[2 * i +1]
        counter += 1
        print("\n", counter, "\nw", w, "\nxi", xi)

    print("\nCode finished after", counter, 'iterations')
    print("xi", xi, "\nw", w)

    return [w, xi]

if __name__ == "__main__":
    Spline_Quadrature()