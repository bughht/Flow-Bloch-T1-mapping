import numpy as np
from crot import crot, crotx, croty, crotz

gamma = 42.58e6  # Hz/T


class Voxel:
    def __init__(self, B0, T1, T2):
        self.T1 = T1
        self.T2 = T2
        self.M = np.array([0, 0, 1], dtype=complex)
        self.B0 = B0
        self.B = B0
        self.freq = gamma*B0
        self.dB = 0
        self.dfreq = 0  # Hz

    def set_dB(self, dB):
        self.dB = dB
        self.dfreq = gamma * dB
        self.B = self.B0+self.dB
        self.freq = gamma*self.B

    def __repr__(self):
        return str(self.M)


class Voxel_Field:
    def __init__(self, B0=1.5, shape=(4, 4, 4), vox_size=(1e-4, 1e-4, 1e-4)):
        self.B0 = B0
        self.shape = shape
        self.V = np.array([[[Voxel(B0, 0.1, 0.6) for k in range(shape[2])]
                          for j in range(shape[1])] for i in range(shape[0])])
        self.vox_size = vox_size

    def apply_gradient(self, G):
        """
        G: gradient strength in T/m
        """
        for i, j, k in np.ndindex(self.shape):
            self.V[i, j, k].set_dB(
                np.dot(G, self.vox_size*np.array([i, j, k])))

    def apply_rf(self, phi, theta, freq, bandwidth=200):
        for i, j, k in np.ndindex(self.shape):
            if self.V[i, j, k].freq >= freq-bandwidth/2 and self.V[i, j, k].freq <= freq+bandwidth/2:
                self.V[i, j, k].M = crot(phi, theta)@self.V[i, j, k].M


if __name__ == "__main__":
    vf = Voxel_Field(shape=(1, 1, 32))
    G = np.array([0, 0, 5e-3])
    vf.apply_gradient(G)
    vf.apply_rf(phi=np.pi/2, theta=0, freq=3870300, bandwidth=200)
    for i, j, k in np.ndindex(vf.shape):
        print(vf.V[i, j, k].B0*gamma, vf.V[i, j, k].df)
