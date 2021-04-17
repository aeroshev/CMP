import numpy as np


global d

def do_something():
    n = 10
    m = 45
    if n or m:
        d = np.array([[1, 2, 3], [4, 5, 6]])
    elif n and m:
        return n, m
    elif n - m > 0:
        n = n - m

    if m + 1 >= 1:
        s = 'do_something'
    elif n * 0 > 0:
        r = np.array([[1, 1, 1, 1]])
    else:
        r = 'skip'
    return n, m
