import numpy as np


class Particle:
    def __init__(self, init_pos, vel):
        self.pos = init_pos
        self.vel = vel

    def update(self, dt):
        self.pos += self.vel*dt

    def __repr__(self):
        return f"Particle(pos={self.pos}, vel={self.vel})"


if __name__ == "__name__":
    p = Particle(np.array([0, 0]), np.array([1, 1]))
    print(p)
    p.update(1)
    print(p)
