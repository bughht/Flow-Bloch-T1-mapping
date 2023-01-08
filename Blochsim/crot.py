import numpy as np
from rot import rotx, roty, rotz, rotz


def rot2crot(Mr):
    T = np.array([[1, 1j, 0],
                  [1, -1j, 0],
                  [0, 0, 1]])
    T_ = np.array([[0.5, 0.5, 0],
                  [-0.5j, 0.5j, 0],
                  [0, 0, 1]])
    return T@Mr@T_


def crot2rot(Mr):
    T = np.array([[1, 1j, 0],
                  [1, -1j, 0],
                  [0, 0, 1]])
    T_ = np.array([[0.5, 0.5, 0],
                  [-0.5j, 0.5j, 0],
                  [0, 0, 1]])
    return T_@Mr@T


def Mr2Mc(Mr):
    T = np.array([[1, 1j, 0],
                  [1, -1j, 0],
                  [0, 0, 1]])
    return T@Mr


def Mc2Mr(Mc):
    T_ = np.array([[0.5, 0.5, 0],
                  [-0.5j, 0.5j, 0],
                  [0, 0, 1]])
    return T_@Mc


def crotx(theta):
    return rot2crot(rotx(theta))


def croty(theta):
    return rot2crot(roty(theta))


def crotz(theta):
    return rot2crot(rotz(theta))
