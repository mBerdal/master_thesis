import numpy as np

def polar_to_vec(r, theta):
    return r*np.array([np.cos(theta), np.sin(theta)])