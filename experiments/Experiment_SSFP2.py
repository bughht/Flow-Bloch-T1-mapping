import numpy as np
import matplotlib.pyplot as plt

import BlochSim

T1 = 1000
T2 = 45
# FA = np.linspace(np.pi/180*5, np.pi/180*65, num=7)
FA = np.pi/180*45
TR = 2.8

N_flip = 50
# generate df from -100 to 100 Hz
df = np.linspace(-180, 180, num=7)

sig_Mz = np.zeros((len(df), N_flip*2))
sig_Mxy = np.zeros((len(df), N_flip*2))
t = np.arange(0, N_flip*2*TR, TR)

for m in range(0, df.size):
    Rflip_0 = BlochSim.yrot(FA)
    Rflip_1 = BlochSim.yrot(-FA)
    Atr, Btr = BlochSim.freeprecess(TR, T1, T2, df[m])
    M = np.array([[0], [0], [-1]])
    for n_pulse in range(N_flip):
        M = Atr@(Rflip_0@M)+Btr
        Msig = np.abs(M[0, 0]+1j*M[1, 0])
        Mz = M[2, 0]
        sig_Mxy[m, n_pulse*2] = Msig
        sig_Mz[m, n_pulse*2] = Mz
        M = Atr@(Rflip_1@M)+Btr
        Msig = np.abs(M[0, 0]+1j*M[1, 0])
        Mz = M[2, 0]
        sig_Mxy[m, n_pulse*2+1] = Msig
        sig_Mz[m, n_pulse*2+1] = Mz

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)

    ax1.plot(t, sig_Mxy[m, :], label='df = %2d' % df[m])
    ax2.plot(t, sig_Mz[m, :], label='df = %2d' % df[m])

ax1.legend()
ax2.legend()
plt.show()
