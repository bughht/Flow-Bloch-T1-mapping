from SeqLoader import MRISequence
import scipy.fftpack as sfft
import numpy as np
import BlochSim as bs
import matplotlib.pyplot as plt
import seaborn as sns
import os


class M:
    def __init__(self, T1, T2, pos) -> None:
        self.T1 = T1
        self.T2 = T2
        self.pos = pos
        self.M = np.array([[0.0], [0.0], [1.0]], dtype=np.float64)

    def flip(self, FA):
        Rflip = bs.yrot(np.deg2rad(FA))
        self.M = Rflip@self.M

    def freeprecess(self, t, Gx, Gy):
        df = Gx*self.pos[0]+Gy*self.pos[1]
        Afp, Bfp = bs.freeprecess(t, self.T1, self.T2, df)
        self.M = Afp @ self.M+Bfp

    def update_pos(self, pos):
        self.pos = pos

    def __repr__(self) -> str:
        return f"M(M={self.M},phase={np.angle(self.M[1]+1j*self.M[2])}, pos={self.pos})"


if __name__ == "__main__":
    seq = MRISequence(os.path.join("sequences_ssfp", "TR2.8_FA5.yaml")).data
    m_test = M(1000, 20, np.array([-32, -32]))

    t = []
    M = []
    t_adc = []
    M_adc = []
    k = np.zeros((128, 128), dtype=complex)

    t_local = 0
    Gx = 0
    Gy = 0
    for ts in seq:
        # print(ts)
        m_test.freeprecess(ts['t']-t_local, Gx, Gy)
        if ts['type'] == "PULSE":
            m_test.flip(ts['FA'])
        if ts['type'] == "GX":
            Gx = ts['G']
        if ts['type'] == "GY":
            Gy = ts['G']
        t_local = ts['t']
        if ts['type'] == "ADC":
            k[ts['kx'], ts['ky']] = m_test.M[0]+1j*m_test.M[1]
            t_adc.append(t_local)
            M_adc.append(m_test.M)
        t.append(t_local)
        M.append(m_test.M)

    plt.figure()
    M = np.array(M)
    M_adc = np.array(M_adc)
    plt.subplot(3, 1, 1)
    plt.plot(t, M[:, 2])
    plt.plot(t_adc, M_adc[:, 2])
    plt.subplot(3, 1, 2)
    plt.plot(t, np.abs(M[:, 0]+1j*M[:, 1]))
    plt.plot(t_adc, np.abs(M_adc[:, 0]+1j*M_adc[:, 1]))
    plt.subplot(3, 1, 3)
    plt.plot(t, np.angle(M[:, 0]+1j*M[:, 1]))
    plt.plot(t_adc, np.angle(M_adc[:, 0]+1j*M_adc[:, 1]))

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(np.abs(k))
    # plt.subplot(2, 1, 2)
    # plt.imshow(np.angle(k))
    plt.subplot(1, 2, 2)
    # plt.imshow(np.log(np.abs(sfft.ifft2(k))))
    plt.imshow(np.abs(sfft.ifft2(k)))
    plt.show()
