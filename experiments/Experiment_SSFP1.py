import numpy as np
import matplotlib.pyplot as plt

import BlochSim

T1 = 1000
T2 = 45
FA = np.linspace(np.pi/180*5, np.pi/180*65, num=7)
TR = 2.8

# generate df from -100 to 100 Hz
df = np.linspace(-400, 400, num=501)
N_flip = 33

sig_ssfp = np.zeros((FA.size, df.size), dtype=complex)
Mz_ssfp = np.zeros((FA.size, df.size))
Mz_history = np.zeros((FA.size, df.size, N_flip))


for m in range(0, FA.size):
    for n in range(0, df.size):
        Rflip_0 = BlochSim.yrot(FA[m])
        Rflip_1 = BlochSim.yrot(-FA[m])
        Atr, Btr = BlochSim.freeprecess(TR, T1, T2, df[n])
        M = np.array([[0], [0], [-.5]])
        for n_pulse in range(N_flip):
            M = Atr@(Rflip_0@M)+Btr
            M = Atr@(Rflip_1@M)+Btr
            Mz_history[m, n, n_pulse] = M[2, 0]
        Msig = M[0, 0]+1j*M[1, 0]
        Mz = M[2, 0]
        sig_ssfp[m, n] = Msig
        Mz_ssfp[m, n] = Mz

    ax1 = plt.subplot(211)
    ax1.plot(df, np.absolute(
        sig_ssfp[m, :]), '-', label='FA = %2d' % int(FA[m]/np.pi*180))

    ax2 = plt.subplot(212)
    ax2.plot(df, Mz_ssfp[m, :], '-',
             label='FA = %2d rad' % int(FA[m]/np.pi*180))

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
plt.show()

plt.plot(Mz_history[0, 0, :])
plt.show()
