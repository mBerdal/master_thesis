import numpy as np
from matplotlib.pyplot import subplots as sbplt
from matplotlib.animation import FuncAnimation as fnanim
import os

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


def file_saver_aux(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)