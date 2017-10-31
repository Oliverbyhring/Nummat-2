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
    print("integrals_c", integrals_c)
    print("Ser legit ut. De basisfunksjonene som er helt inneholdt i intervallet integreres til 1, de mot kantene har deler som 'ligger utenfor'")

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
    print("xi", xi)
    # Denne er for å få resten til å fungere inntil vi fikser det over!!!!!!!!!:
    xi = np.linspace(0,6,n)

    w = np.zeros(n) # Denne initialiseres som fra optimal quad-boka
    for i in range(n):
        w[i] = integrals_c[2*i] + integrals_c[2*i+1]

    # 3) Generate basis functions, evaluer og finn partiellderiverte av F
    basis = sp.BSplineBasis(order=p+1, knots=T) #Burde denne lagres eksternt for å forbedre kjøretid?
    print("basis", basis)
    return w, xi, n, integrals_c

def Assembly(basis, I, w, xi, n):
    # 1) Lag en matrise med basisfunksjonene evaluert med gitte w og xi
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

    # 2) Beregn F-matrisen gange omega-vektor, uten integral
    Fn = B.dot(w)

    # 3) Sett sammen en Jacobi med redusert bandwidth
    naive_jacobi = np.concatenate((dFdw, dFdxi), axis=1)
    print("naive_jacobi\n", naive_jacobi)
    split_dFdw = np.hsplit(dFdw, n)
    split_dFdxi = np.hsplit(dFdxi, n)
    jacobian = np.concatenate((split_dFdw[0], split_dFdxi[0]), axis=1)
    for i in range(1,n):
        jacobian = np.concatenate((jacobian, split_dFdw[i], split_dFdxi[i]), axis=1)
    print("jacobian\n", jacobian)
    print("But is the jacobian a numpy array now?")
    # Invert Jacobian
    inv_jacobi = np.linalg.inv(jacobian) #Jacobian var singular fordi x ivar fucked up
    print("inv_jacobi\n", inv_jacobi)

    return Fn, inv_jacobi

def Spline_Quadrature():
    T = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6]
    p = 3
    w, xi, n, integrals_c = Prepare_Data(T, p)
    # T er endret men brukes ikke videre ned i koden så returneres ikke. For å vise at vi ikke trenger T lengre:
    T = [0]

    ############################
    Fn, dFn_invers = Assembly()

    # zk = [w, xi]
    counter = 0
    convergence_criteria = Fn - integrals_c
    while np.linalg.norm(convergence_criteria, ord=np.inf) > TOLERANCE:
        Fn, dFn_invers = Assembly()
        dx = dFn_invers.dot(Fn-integrals_c)
        zk = zk - dx
        counter += 1
    print(counter, 'iterations')

    return zk

if __name__ == "__main__":
    Spline_Quadrature()