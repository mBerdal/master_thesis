import numpy as np

def polar_to_vec(r, theta):
    return r*np.array([np.cos(theta), np.sin(theta)])

def normalize(vec):
    if not (vec == 0).all():
        return vec/np.linalg.norm(vec)
    return vec

def plot_vec(ax, vec, start_point=np.zeros((2, )), clr="black", alpha=1):
    ax.plot(*np.hstack((start_point.reshape(2, 1), start_point.reshape(2, 1) + vec.reshape(2, 1))), color=clr, alpha=alpha)