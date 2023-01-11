# Extended Phase Graphs
# Rf excitation: M'=R(alpha,theta)@M
# Gradient-inducedrotation: M'=Rz(gamma(G*r+delta_B0))@M
# Relaxation: M'= A(t,T1,T2)M+B(t,T1,T2)

import numpy as np
from crot import crotx, croty, crotz, crot


def M2Q_1D(M_1D):
    # M_1D: 1D array of complex numbers
    # Q_1D: 1D array of complex numbers
    assert M_1D.shape[0] == 3 and len(
        M_1D.shape) == 2, "M_1D must be a 3xN array"
    n = M_1D.shape[1]
    Q_1D = np.fft.fft(M_1D, axis=1,)
    return Q_1D


def precession(Q, theta):
    return crotz(theta)@Q


def gradients(Q, gamma, G, r, delta_B0):
    return crotz(gamma*(G*r+delta_B0))@Q


if __name__ == "__main__":
    M = np.zeros([3, 8], dtype=complex)
    M[2] = 1
    Q = M2Q_1D(M)
    print(Q)
