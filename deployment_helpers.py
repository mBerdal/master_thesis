import numpy as np
from helpers import rot_z_mat as R_z


def get_neighbor_forces(K_n, MIN):
    vecs_to_neighs = [
        MIN.get_vec_to_other(n).reshape(2, 1) for n in MIN.neighbors if not (MIN.get_vec_to_other(n) == 0).all()
    ]
    return get_generic_force_vector(vecs_to_neighs, K_n)

def get_obstacle_forces(K_o, MIN, ENV):
    for s in MIN.sensors:
        s.sense(ENV)
    vecs_to_obs = [
        (R_z(MIN.heading)@R_z(s.host_relative_angle)@s.measurement.get_val())[:2]
        for s in MIN.sensors if s.measurement.is_valid()
    ]
    return get_generic_force_vector(vecs_to_obs, K_o)

def get_generic_force_vector(vecs, gain):
    try:
        mat = np.concatenate(vecs, axis=1)
        return -gain*np.sum(mat/np.linalg.norm(mat, axis=0)**3, axis=1)
    except ValueError:
        return np.zeros((2, ))

class AtLandingConditionException(Exception):
    """
    Raised when the exploring MIN fulfills its landing condition
    """