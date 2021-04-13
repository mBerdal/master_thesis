import numpy as np
from matplotlib.pyplot import subplots as sbplt
from matplotlib.animation import FuncAnimation as fnanim
import os

def xi_model(d, d_perf, d_none, xi_max, omega=None, phi=None):
    if d < d_perf:
      return xi_max
    if d > d_none:
      return 0

    if omega is None:
        omega = np.pi/(d_none - d_perf)
    if phi is None:
        phi = -np.pi*d_perf/(d_none - d_perf)
    return (xi_max/2)*(1+np.cos(omega*d + phi))

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

def clamp(F, limit):
    norm_F = np.linalg.norm(F)
    if norm_F > limit:
      return limit*F/norm_F
    return F

def clamp01(scalar):
    if scalar < 0:
        return 0
    if scalar > 1:
        return 1
    return scalar

def plot_vec(axis, vec, startpoint=np.zeros((2, )), clr="black", alpha=1):
    """

    Args:
        vec (ndarray): array of shape (2, ) containing vector end porint.
        axis (matplotlib.axis): axis on which to perform the plotting.
        color (string): Facecolor of arrow. Defaults to None.
    """
    return axis.plot(*np.hstack((startpoint.reshape(2, 1), startpoint.reshape(2, 1) + vec.reshape(2, 1))), color=clr, alpha=alpha)[0]

def plot_configuration(env, scs, mins, sub_dir_name=None):
    fig, ax = sbplt()
    env.plot(ax)
    scs.plot(ax)
    
    for mn in mins:
      mn.plot(ax)
      mn.plot_traj_line(ax)
    
    ax.axis("equal")
    if not sub_dir_name is None:
        dir_name = "plots/" + sub_dir_name
        file_saver_aux(dir_name)
        fig.savefig(dir_name + "/config.png", bbox_inches="tight")
    return ax

def animate_configuration(env, scs, mins, sub_dir_name):
    fig, ax = sbplt()

    offset, min_counter = [0], [0]

    def init():
      scs.plot(ax)
      env.plot(ax)
      artists = []
      for mn in mins:
        artists += mn.plot(ax)
        artists += (mn.plot_traj_line(ax), )
        mn.plot_pos_from_pos_traj_index(0)
      return artists

    def animate(i):
      if i - offset[0] >= mins[min_counter[0]]._pos_traj.shape[1]:
        offset[0] += mins[min_counter[0]]._pos_traj.shape[1]
        min_counter[0] += 1

      return mins[min_counter[0]].plot_pos_from_pos_traj_index(i - offset[0])



    anim = fnanim(fig, animate, init_func=init, interval=2, blit=False)
    if not sub_dir_name is None:
        dir_name = "animations/" + sub_dir_name
        file_saver_aux(dir_name)
        animation_name = dir_name + "/config_animation.gif"
        print("Saving animation")
        anim.save(animation_name)
        print(f"Animation saved to {animation_name}")

def plot_speed_trajs(mins, sub_dir_name):
    fig, ax = sbplt()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Speed [m/s]")
    for MIN in mins:
        ax.plot(MIN.get_timeline(), MIN.get_speed_traj())
    ax.legend([f"MIN {MIN.ID}" for MIN in mins])

    if not sub_dir_name is None:
        dir_name = "plots/" + sub_dir_name
        file_saver_aux(dir_name)
        fig.savefig(dir_name + "/speed_traj.png", bbox_inches="tight")
    return ax

def plot_gains(beacons, sub_dir_name):
    fig, ax = sbplt(2, sharex=True)
    ax = ax.flatten()

    xs = [b.ID for b in beacons]
    k_is = [b.k for b in beacons]
    a_is = [b.a for b in beacons]

    ax[0].bar(xs, k_is, color="red")
    ax[0].set_ylabel(r"$\kappa_{i}$")

    ax[1].bar(xs, a_is, color="blue")
    ax[1].set_ylabel(r"$\alpha_{i}$")

    ax[1].set_xlabel("$i$ (ID)")

    if not sub_dir_name is None:
        dir_name = "plots/" + sub_dir_name
        file_saver_aux(dir_name)
        fig.savefig(dir_name + "/gains.png", bbox_inches="tight")
    return ax


def file_saver_aux(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)



### SAMPLE COVARIANCE STUFF

def sample_mean(samples, weights=None, get_sum_weights=False):
    
    """Computes sample mean (multi-dim, weighted)

    Args:
        samples (ndarray): k-by-N matrix where
        columns correspond to a single sample vector

        weights (ndarray, optional): 1-by-N array of weights
        associated with each sample

        get_sum_weights (bool, optional): wether or not the
        sum of weights should be returned

    Returns:
        ndarray, (float): sample mean of shape k-by-1
        , (sum of weights if get_sum_weights is set to True)
    """

    return np.average(
        samples, axis=1, weights=weights, returned=get_sum_weights
    ).reshape(-1, 1)

def sample_covar_mat(samples, weights=None):
    """Computes sample covariance matrix

    Args:
        samples (ndarray): 2-by-N matrix where
        columns correspond to a single sample vector

    Returns:
        [ndarray]: N-by-N sample covariance matrix
    """
    N = samples.shape[1]

    assert weights is None or weights.shape[0] == N and np.sum(weights) == 1,\
        "must have as many weights as samples, and weights must sum up to 1"

    if weights is None:
        weights = np.ones((N, ))/N

    W = 1/(1 - np.sum(np.power(weights, 2)))
    wm = sample_mean(samples, np.tile(weights, (2, 1)))

    t_11 = np.sum(weights*(samples[0, :] - wm[0])**2)
    t_22 = np.sum(weights*(samples[1, :] - wm[1])**2)
    t_12 = np.sum(weights*(samples[0, :] - wm[0])*(samples[1, :] - wm[1]))

    return W*np.array([
        [t_11, t_12],
        [t_12, t_22]
    ])
    
def generalized_sample_variance(samples):
    return np.linalg.det(sample_covar_mat(samples))

def total_sample_variance(samples):
    return np.trace(sample_covar_mat(samples))