import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def T1_curve(t, T1, A, B):
    return A-B*np.exp(-t*T1)


def MOLLI_fit(t, Mz):
    params = curve_fit(T1_curve, t, Mz, p0=[1, 1, 1])
    [T1_star, A, B] = params[0]
    T1 = (B/A-1)*T1_star
    return T1_star, T1, A, B


if __name__ == "__main__":
    # t = np.array([200, 1200, 2200, 3200, 4200, 300, 1300, 2300]) * 1e-3
    # Mz = np.array([-0.55, 0.39, 0.63, 0.71, 0.73, -0.40, 0.42, 0.64])

    # Fit
    T1_star, T1, A, B = MOLLI_fit(t, Mz)
    print(T1_star, T1, A, B)

    # t_fit = np.arange(0, 5e3, 1)
    t_fit = np.arange(0, 5, 1e-5)
    Mz_fit = T1_curve(t_fit, T1_star, A, B)
    plt.plot(t_fit, Mz_fit)
    plt.scatter(t, Mz)
    plt.show()
