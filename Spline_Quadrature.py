################################################################################
import time
import numpy as np
import scipy as sp
import splipy as spl
np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)


################################################################################

# EVEN:
# Vi må garra bruke sparse.linalg.spsolve og sparse.csr_matrix, som er
# scipy-funksjoner oppgitt i d). Gjetter på at det har med at vi får
# 'numpy.linalg.linalg.LinAlgError: Matrix is singular' å gjøre.

# Sist oppdatert 5.11.17 av Sivert

################################################################################

TOLERANCE = 1e-11

def Prepare_Data(T, p): # (knot vector, degree of polynomial)

    # 0) Prepare knot vector
    if (len(T) - p - 1) % 2: # n=len(T)-p-1. We add a knot if n is not even
        new_T = T[:p+1]
        np.append(new_T,(T[p] + T[p+1])/2)
        new_T += T[p+1:]
        T = new_T

    n = int((len(T) - p - 1) / 2)

    # 1) Calculate exact integrals
    integrals_c = np.zeros(2*n)
    for i in range(2*n):
        integrals_c[i] = (T[i+p+1] - T[i])/(p+1)

    # 2) Generate initial xi and w
    xi = np.zeros(n)
    tau_abscissa = np.zeros(2*n)
    for i in range(2*n):
        tau_abscissa[i] = sum(T[i+1:i+p+1])/p
    for i in range(n):
        xi[i] = (tau_abscissa[2 * i] + tau_abscissa[2 * i + 1]) / 2

    w = np.zeros(n)
    for i in range(n):
        w[i] = integrals_c[2*i] + integrals_c[2*i+1]

    # 3) Generate basis functions, evaluate and get partial derivatives of F
    basis = spl.BSplineBasis(order=p + 1, knots=T)

    return basis, integrals_c, w, xi, n


def Assembly(basis, integrals_c, w, xi, n):

    # 1) Lag en N-matrise med basisfunksjonene N evaluert i xi-punktene
    N = np.array(basis.evaluate(xi)) # N.shape = (n evaluation points, 2n basis functions)
    # Vi venter med å transponere siden det gjør det lettere å flette sammen en jacobian

    # 2) Beregn Fn
    Fn = N.transpose().dot(w) - integrals_c

    # 3) Beregn Jacobien med redusert bandwidth og sparse. dFdw tilsvarer N, dFdxi[i][j] tilsvarer w[i]*N[j]'(xi[i]).
    J = np.zeros((2*n, 2*n))
    dFdxi = np.array(basis.evaluate(xi, d=1)).transpose()*w # Elementwise vekting av kolonnene i N'(xi) med element i w
    dFdxi = dFdxi.transpose() # Gir dobbel transponering merkbart lengre kjøretid????

    for i in range(n):
        J[2*i] = N[i] # dF/dw tilsvarer N
        J[2*i+1] = dFdxi[i]
    J = J.transpose()

    return Fn, J


def Spline_Quadrature(T,p):
    #T = [0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4]
    #p = 3 # Antall repeterende elemter i T, minus 1
    basis, integrals_c, w, xi, n = Prepare_Data(T, p) # T er endret men brukes ikke videre i koden så returneres ikke
    #HERRE MÅ FIKSES!
    dz = np.array([10000])
    counter = 0

    while abs(np.linalg.norm(dz, ord=np.inf)) > TOLERANCE and counter < 500:
        Fn, J = Assembly(basis, integrals_c, w, xi, n)
        J = sp.sparse.csr_matrix(J)
        dz = sp.sparse.linalg.spsolve(J, Fn) # dz er på formen [ w_1 xi_1 x_2 xi_2 ... ]

        for i in range(n):
            w[i] -= dz[2*i]
            xi[i] -= dz[2 * i +1]
        counter += 1
        print("\n", counter, "\nw", w, "\nxi", xi)

    print("\nCode finished after", counter, 'iterations')

    return [w, xi] # noen spesiell grunn til at disse retureres i vektor?
