# Gammel Assembly med avansert splitting av partiellderiverte for å lage Jacobian
def Assembly(basis, integrals_c, w, xi, n):
    # 1) Lag en N-matrise med basisfunksjonene N evaluert i xi-punktene
    N = np.array(basis.evaluate(xi)).transpose() # N.shape = (2n basis functions, n evaluation points)
    print("N\n", N)
    if N.shape != (2*n, n):
        print("Not 2nXn! Du har glemt a order=p+1!")

    # Check!
    # 2) Beregn F-matrisen gange omega-vektor, uten integral
    Fn = N.dot(w) - integrals_c
    print(Fn)

    # 3) Beregn Jacobien med redusert bandwidth og sparse
    J = np.zeros((2*n, 2*n)) #Lagre enkelt først og transpose etterpå?
    for i in range(n):
        Fn=Fn
    dFdw = N  # dFdw is equal to B!
    print("dFdw\n", dFdw)
    N_der = np.array(basis.evaluate(xi, d=1)).transpose()
    print("N_der\n", N_der)
    dFdxi = N_der*w # Dette er ikke matrix multiplication, men elementwise vekting av kolonnene i N_der med elementene i w
    print("dFdxi\n", dFdxi)
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
