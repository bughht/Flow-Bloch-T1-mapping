from SeqLoader import MRISequence
import numpy as np
import BlochSim as bs
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")

# Load sequence
name = "MOLLI_533_dt_TR2.8_FA30_N75_SA_prep"
seq = MRISequence(os.path.join("sequences_old", name+".yaml")).data[name]

# Simulate Params
T1 = 1000
T2 = 45
M = np.array([[0.0], [0.0], [1.0]], dtype=np.float64)
t_state = np.zeros(len(seq)*2)
M_state = np.zeros((len(seq)*2, 3))
M_state[0, :] = M.flatten()

# Simulate
prev_t = 0
for idx, pulse in enumerate(seq):
    Afp, Bfp = bs.freeprecess(pulse["t"]-prev_t, T1, T2, 0)
    Rflip = bs.yrot(np.deg2rad(pulse["FA"]))
    M_ = np.matmul(Afp, M)+Bfp
    M = Rflip@M_
    M_state[idx*2, :] = M_.flatten()
    M_state[idx*2+1, :] = M.flatten()
    t_state[idx*2], t_state[idx*2+1] = pulse["t"], pulse["t"]
    prev_t = pulse["t"]

# Plot
plt.subplot(311)
plt.plot(t_state, M_state[:, 2])

plt.subplot(312)
plt.plot(t_state, np.abs(M_state[:, 0]+1j*M_state[:, 1]))

plt.subplot(313)
plt.plot(t_state, np.angle(M_state[:, 0]+1j*M_state[:, 1]))
plt.show()
