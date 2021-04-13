import numpy as np

def get_agent_i_local_density(i, N_i, agent_positions, R_d):
    n_i = len(N_i)
    if n_i == 0:
        return 1
    r_ij_bar = np.mean(
        np.linalg.norm(
            agent_positions[:, i].reshape(2, 1) - agent_positions[:, N_i], axis=1
        )
    )
    return 1 + (R_d/r_ij_bar)*n_i

def get_agent_i_pressure(R, T_i, rho_i):
    return rho_i*R*T_i

def get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, flow_var, direction):
    assert direction == "x" or direction == "y"
    n_i = len(N_i)
    if n_i == 0:
        return 0
    r_ijs = np.linalg.norm(agent_positions[:, i].reshape(2, 1) - agent_positions[:, N_i], axis=1)
    theta_ijs = np.arctan2(
        agent_positions[1, i] - agent_positions[1, N_i],
        agent_positions[0, i] - agent_positions[0, N_i]
    )
    tmp = (1/n_i)*np.sum(((flow_var[i] - flow_var[N_i])/r_ijs))
    return tmp*(np.cos(theta_ijs) if direction == "x" else np.sin(theta_ijs))


def get_agent_i_u_dot(agent_positions, agent_us, agent_vs, agent_ps, rho_i, i, N_i, f_x_i):
    return (-(
            agent_us[i]*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_us, "x") +\
            agent_vs[i]*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_us, "y") +\
            (1/rho_i)*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_ps, "x")
        ) + f_x_i)

def get_agent_i_v_dot(agent_positions, agent_us, agent_vs, agent_ps, rho_i, i, N_i, f_y_i):
    return (-(
            agent_us[i]*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_vs, "x") +\
            agent_vs[i]*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_vs, "y") +\
            (1/rho_i)*get_agent_i_spatial_derivative_of_flow_var_in_dir(i, N_i, agent_positions, agent_ps, "y")
        ) + f_y_i)

def get_agent_i_acc(i, N_i, agent_positions, agent_us, agent_vs, agent_ps, f_x_i, f_y_i, R_d):
    
    rho_i = get_agent_i_local_density(i, N_i, agent_positions, R_d)

    return np.array([
        get_agent_i_u_dot(agent_positions, agent_us, agent_vs, agent_ps, rho_i, i, N_i, f_x_i),
        get_agent_i_v_dot(agent_positions, agent_us, agent_vs, agent_ps, rho_i, i, N_i, f_y_i)
    ])

def get_agent_i_nxt_velocity(i, N_i, agent_states, f_x_i, f_y_i, R_d, R_c, C, D, dt):
    agent_positions = agent_states[0:2, :].reshape(2, -1)
    agent_us = agent_states[2, :]
    agent_vs = agent_states[3, :]
    agent_ps = agent_states[4, :]

    acc = get_agent_i_acc(i, N_i, agent_positions, agent_us, agent_vs, agent_ps, f_x_i, f_y_i, R_d)
    r_ij_bar = np.mean(
        np.linalg.norm(
            agent_positions[:, i].reshape(2, 1) - agent_positions[:, N_i], axis=1
        )
    )
    F = C - np.power(r_ij_bar/R_c, D)
    return (F*agent_states[2:3, i] + acc*dt).reshape(2, 1)


if __name__ == "__main__":
    R_c = 4
    R_d = 2
    R_s = 2
    R = 3
    dt = 1/20
    B = 0
    C = 1
    D = 12
    v_th = 2
    a_th = 0.5
    t = 30



    d_mark = R_s-B
    K = d_mark/(2*R_s - d_mark)
    T = 1+(1-K)