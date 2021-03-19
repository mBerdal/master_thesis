import numpy as np

def euler_int(state, state_dot, dt):
    return state + dt*state_dot

def polar_to_vec(r, theta):
    return r*np.array([np.cos(theta), np.sin(theta)])

def get_vector_angle(vec):
    if vec.ndim == 1:
        return np.arctan2(vec[1], vec[0])
    return np.arctan2(vec[1, :], vec[0, :])

def normalize(vec):
    if not (vec == 0).all():
        return vec/np.linalg.norm(vec)
    return vec

def get_smallest_signed_angle(ang):
    return np.mod(ang + np.pi, 2*np.pi) - np.pi

def rot_z_mat(ang):
    return np.array([
        [np.cos(ang), -np.sin(ang), 0],
        [np.sin(ang),  np.cos(ang), 0],
        [     0     ,      0      , 1]
    ])

def rot_mat_2D(ang):
  return rot_z_mat(ang)[:2, :2]

def plot_vec(axis, vec, startpoint=np.zeros((2, )), clr="black", alpha=1):
    """

    Args:
        vec (ndarray): array of shape (2, ) containing vector end porint.
        axis (matplotlib.axis): axis on which to perform the plotting.
        color (string): Facecolor of arrow. Defaults to None.
    """
    return axis.plot(*np.hstack((startpoint.reshape(2, 1), startpoint.reshape(2, 1) + vec.reshape(2, 1))), color=clr, alpha=alpha)[0]