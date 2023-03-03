import numpy as np
import matplotlib.pyplot as plt

import BlochSim

T1 = 1000
T2 = 45
FA = np.linspace(np.pi/180*5, np.pi/180*65, num=7)
TR = 2.8

# generate df from -100 to 100 Hz
df = np.linspace(-400, 400, num=501)

# TE = np.array([0., 2.5, 5., 7.5, 10.])
TE = 0

sig_ssfp = np.zeros((FA.size, df.size), dtype=complex)

for m in range(0, FA.size):
    for n in range(0, df.size):
        Msig, Mss = BlochSim.sssignal(FA[m], T1, T2, TE, TR, df[n])
        sig_ssfp[m, n] = Msig

    ax1 = plt.subplot(211)
    ax1.plot(df, np.absolute(
        sig_ssfp[m, :]), '-', label='FA = %2d rad' % int(FA[m]/np.pi*180))

    ax2 = plt.subplot(212)
    ax2.plot(df, np.angle(sig_ssfp[m, :]), '-',
             label='FA = %2d rad' % int(FA[m]/np.pi*180))

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
plt.show()
