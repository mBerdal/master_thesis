import numpy as np

def xi_model(d, d_perf, d_none, xi_max, omega=None, phi=None):
    if omega is None:
        omega = np.pi/(d_none - d_perf)
    if phi is None:
        phi = -np.pi*d_perf/(d_none - d_perf)

    ret =  (xi_max/2)*(1+np.cos(omega*d + phi))
    ret[d < d_perf] = xi_max
    ret[d > d_none] = 0
    return ret

def euler_int(state, state_dot, dt):
    return state + dt*state_dot

if __name__ == "__main__":
    leader_positions = np.array([
        [-5, 5, 5, -5],
        [-5, -5, 5, 5]
    ]) + np.random.uniform(-1, 1, size=(2, 4))



    beacon_pos = np.array([[0], [-15]])

    v = np.inf*np.ones((2, 1))
    while np.linalg.norm(v) > 1e-6:
        d = np.linalg.norm(beacon_pos - leader_positions, axis=0)
        xi = xi_model(d, 4, 16, 1)
        adjacency_vector = (xi > 0)*1
    
        v = -np.sum(adjacency_vector*(beacon_pos - leader_positions), axis=1, keepdims=True)
        beacon_pos = euler_int(beacon_pos, v, 0.001)
    leader_positions = np.concatenate((leader_positions, beacon_pos), axis=1)
    
    import matplotlib.pyplot as plt
    print(leader_positions)
    plt.scatter(*leader_positions)
    plt.show()