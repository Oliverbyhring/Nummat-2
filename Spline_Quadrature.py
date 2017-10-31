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
    print("T =", T)
    n = int((len(T) - p - 1) / 2)
    print("2n =", 2*n)
    # 1) Calculate exact integrals
    integrals_c = np.zeros(2*n)
    for i in range(2*n):
        integrals_c[i] = (T[i+p+1] - T[i])/(p+1)
    print("integrals_c", integrals_c)
    print("Ser legit ut. De basisfunksjonene som er helt inneholdt i intervallet integreres til 1, de mot kantene har deler som 'ligger utenfor'")

    # 2) Generate initial xi and initial w
    # There must be n initial guesses of xi_distributed over the intervall. Using Greville.
    xi = np.zeros(n)
    tau_abscissa = np.zeros(2*n)
    for i in range(2*n):
        tau_abscissa[i] = sum(T[i+1:i+p+1])/p
    for i in range(n):
        xi[i] = (tau_abscissa[2 * i] + tau_abscissa[2 * i + 1]) / 2
    print("xi", xi)

    w = np.zeros(n) # Denne initialiseres også som fra optimal quad-boka
    for i in range(n):
        w[i] = integrals_c[2*i] + integrals_c[2*i+1]

    # 3) Generate basis functions, evaluer og finn partiellderiverte av F
    basis = sp.BSplineBasis(order=p+1, knots=T) #Burde denne lagres eksternt for å forbedre kjøretid?
    print("basis", basis)
    return basis, integrals_c, w, xi, n

def Assembly(basis, integrals_c, w, xi, n):
    # 1) Lag en N-matrise med basisfunksjonene N evaluert i xi-punktene
    N = np.array(basis.evaluate(xi)) # N.shape = (n evaluation points, 2n basis functions)
    # Vi venter med å transpose siden dette gjør det lettere å flette sammen en fancy jacobian

    # 2) Beregn F-matrisen gange omega-vektor, uten integral
    Fn = N.transpose().dot(w) - integrals_c
    print("Fn", Fn)

    # 3) Beregn Jacobien med redusert bandwidth og sparse
    J = np.zeros((2*n, 2*n)) #Lagre enkelt først og transpose etterpå

    # dFdw tilsvarer N som vi allerede har beregnet
    # dFdxi[i][j] tilsvarer w[i]*N[j]'(xi[i]). Her er den ikke transponert enda
    dFdxi = np.array(basis.evaluate(xi, d=1)).transpose()*w # Dette er elementwise vekting av kolonnene i N'(xi) med elementene i w
    dFdxi = dFdxi.transpose() # Hvor lang tid tar da dette mon tro????
    for i in range(n):
        J[2*i] = N[i] # dF/dw tilsvarer N
        J[2*i+1] = dFdxi[i]
    J = J.transpose()
    print("J", J)

    #naive_jacobi = np.concatenate((N.transpose(), dFdxi.transpose()), axis=1)
    #print("naive_jacobi for comparison\n", naive_jacobi)
    print("But is the jacobian a numpy array now?")

    # Gjør Jacobian sparse og fancy og sånn. Kan det gjøres før og bedre?
    # Invert Jacobian
    inv_jacobi = np.linalg.inv(J)
    print("inv_jacobi\n", inv_jacobi)

    return Fn, inv_jacobi

def Spline_Quadrature():
    T = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6]
    p = 3
    basis, integrals_c, w, xi, n = Prepare_Data(T, p)
    # T er endret men brukes ikke videre ned i koden så returneres ikke.

    # Alternativ 1:
    zk = [xi, w]
    # og så shuffler man rundt på dz hver gang. Tar litt tid men bedre enn å endre på alt som skjer i Assembly

    # Alternativ 2: zk er en glidelås av xi og w
    #zk = np.zeros(2*n)
    #for i in range(n):
    #   zk[2*i] = xi[i]
    #    zk[2*i+1] = w[i]
    #print("zk_0", zk)
    # Dette må i så fall implementeres gjennom assembly

    dz = np.array([10000])
    counter = 0
    # one would like to add additional logic, such as put a maximum number of iterations on the computation of δz k or break if ∂F becomes singular.
    while abs(np.linalg.norm(dz, ord=np.inf)) > TOLERANCE:
        Fn, dFn_invers = Assembly(basis, integrals_c, w, xi, n)
        dz = dFn_invers.dot(Fn-integrals_c)
        # Okei dette er hovedspørsmålet nå. Hva faen er dz og hvordan oppdaterer jeg w og xi på en fornuftig måte?????
        print("dz", -dz)
        # Antar at dz må være på formen [ xi_1 w_1 xi_2 w_2 ... xi_n w_n ]
        time.sleep(1)
        for i in range(n):
            xi[i] -= dz[2*i]
            w[i] -= dz[2*i-1]

        # zk -= dz
        counter += 1
    print(counter, 'iterations')

    return zk

if __name__ == "__main__":
    Spline_Quadrature()