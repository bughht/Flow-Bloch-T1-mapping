import numpy as np
import Blochsim

if __name__ == "__main__":
    M = np.array([0, 0, 1])
    print(Blochsim.rotx(np.pi/2)@M)
