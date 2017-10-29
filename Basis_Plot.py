import numpy as np
import matplotlib.pyplot as plt
import splipy as sp


def Basis_Plot():
    #Fra oppgave: the order is p + 1, where p is the polynomial degree of the spline
    # p can maximally be number of repeated points + 1 ?
    # create a set of B-spline basis functions
    basis1 = sp.BSplineBasis(order=3, knots=[0, 0, 0, 1, 2, 3, 4, 4, 4])
    basis2 = sp.BSplineBasis(order=3, knots=[0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4])
    basis3 = sp.BSplineBasis(order=4, knots=[0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4])
    basis4 = sp.BSplineBasis(order=4, knots=[0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4])

    # 150 uniformly spaced evaluation points on the domain (0,4)
    t = np.linspace(0, 4, 150)

    # evaluate *all* basis functions on *all* points t. The returned variable B is a matrix
    B1 = basis1.evaluate(t)  # Bi.shape = (150,6), 150 visualization points, 6 basis functions
    B2 = basis2.evaluate(t)
    B3 = basis3.evaluate(t)
    B4 = basis4.evaluate(t)
    np.set_printoptions(suppress=True, linewidth=np.nan, threshold=np.nan)
    print(B1)
    # plot the basis functions

    plt.figure()

    plt.subplot(221)
    plt.title("[0, 0, 0, 1, 2, 3, 4, 4, 4]")
    plt.plot(t, B1)
    plt.axis('off')

    plt.subplot(222)
    plt.title("[0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4]")
    plt.plot(t, B2)
    plt.axis('off')

    plt.subplot(223)
    plt.title("[0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4]")
    plt.plot(t, B3)
    plt.axis('off')

    plt.subplot(224)
    plt.title("[0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4]")
    plt.plot(t, B4)
    plt.axis('off')
    """
    plt.plot(t, B1)
    plt.figure()
    plt.plot(t, B2)
    plt.figure()
    plt.plot(t, B3)
    plt.figure()
    plt.plot(t, B4)
    """
    plt.show()


if __name__ == "__main__":
    Basis_Plot()
