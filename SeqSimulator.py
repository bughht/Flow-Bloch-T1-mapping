from SeqLoader import MRISequence
import scipy.fftpack as sfft
import numpy as np
import BlochSim as bs
import matplotlib.pyplot as plt
import seaborn as sns
import os
gamma = 42.577478518e6  # Hz/T


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
        df = gamma*(Gx*self.pos[0]+Gy*self.pos[1])
        Afp, Bfp = bs.freeprecess(t, self.T1, self.T2, df)
        self.M = Afp @ self.M+Bfp

    def update_pos(self, pos):
        self.pos = pos

    def __repr__(self) -> str:
        return f"M(M={self.M},phase={np.angle(self.M[1]+1j*self.M[2])}, pos={self.pos})"


if __name__ == "__main__":
    seq = MRISequence(os.path.join("sequences_ssfp",
                                   "TR2.8_FA20_FOV500_K64_center_first.yaml")).data
    #    "TR2.8_FA20_FOV500_K64.yaml")).data
    ratio = 500/64
    x_rate = 1
    y_rate = 1
    m_test = M(1000, 30, np.array([20*ratio*x_rate, -0*ratio*y_rate]))

    t = []
    M = []
    t_adc = []
    M_adc = []
    Gx_h = []
    Gy_h = []
    k = np.zeros((64, 64), dtype=complex)

    t_local = 0
    Gx = 0
    Gy = 0
    cnt_adc = 0
    now_adc = False
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
            if not now_adc:
                now_adc = True
                cnt_adc += 1
            k[ts['kx'], ts['ky']] = m_test.M[0]+1j*m_test.M[1]
            if (cnt_adc % 2 == 0):
                k[ts['kx'], ts['ky']] *= np.exp(1j*np.pi)
            t_adc.append(t_local)
            M_adc.append(m_test.M)
        else:
            if now_adc:
                now_adc = False
        t.append(t_local)
        Gx_h.append(Gx)
        Gy_h.append(Gy)
        M.append(m_test.M)

    plt.figure()
    k_meshgrid_x, k_meshgrid_y = np.meshgrid(range(64), range(64))
    Ex = k[k_meshgrid_x, k_meshgrid_y].real
    Ey = k[k_meshgrid_x, k_meshgrid_y].imag
    plt.quiver(k_meshgrid_x, k_meshgrid_y, Ex, Ey)

    plt.figure()
    M = np.array(M)
    M_adc = np.array(M_adc)
    plt.subplot(4, 1, 1)
    plt.plot(t, M[:, 2])
    plt.plot(t_adc, M_adc[:, 2])
    plt.subplot(4, 1, 2)
    plt.plot(t, np.abs(M[:, 0]+1j*M[:, 1]))
    plt.plot(t_adc, np.abs(M_adc[:, 0]+1j*M_adc[:, 1]))
    plt.subplot(4, 1, 3)
    plt.plot(t, np.angle(M[:, 0]+1j*M[:, 1]))
    plt.plot(t_adc, np.angle(M_adc[:, 0]+1j*M_adc[:, 1]))
    plt.subplot(4, 1, 4)
    plt.plot(t, Gx_h)
    plt.plot(t, Gy_h)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(np.abs(k))
    # plt.subplot(2, 1, 2)
    # plt.imshow(np.angle(k))
    plt.subplot(1, 2, 2)
    # plt.imshow(np.log(np.abs(sfft.ifft2(k))))
    plt.imshow(np.abs(sfft.fftshift(sfft.ifft2(k))))
    plt.show()
