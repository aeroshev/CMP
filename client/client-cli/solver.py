import numpy as np


def solver(ai, af, w):
    # Make increment tables
    # N=1, E=2, S=3, W=4
    I = np.array([[0, 1, 0 - 1]])
    J = np.array([[1, 0 - 1, 0]])

    a = ai
    m = np.array([[]])
    return m

print(solver(0, 0, 0))
