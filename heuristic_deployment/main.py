from environment import Env
from beacon import Beacon
from min import Min, MinState
from helpers import polar_to_vec as p2v, plot_vec

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate(dt, mins, SCS, env, show_decisions_for = []):
  SCS.insert_into_environment(env)
  beacons = [SCS]

  for mn in mins:
    mn.insert_into_environment(env)

    mn.state = MinState.FOLLOWING
    print(f"min {mn.ID} taking off")
    heading_vec = mn.get_bearing_vec_to_other(beacons[-1])
    mn.set_heading_and_speed(heading_vec, speed=2)
    while mn.state == MinState.FOLLOWING:
      if mn.get_RSSI(beacons[-1]) > np.exp(-0.2):
        mn.state = MinState.EXPLORING
      else: mn.do_step(dt)

    neighs = mn.get_neighbors(beacons)
    bearing_vecs_to_neighs = np.array([
      mn.get_bearing_vec_to_other(neigh) for neigh in neighs
    ])
    num_neighs_of_neighs = np.array([
      neigh.get_num_neighbors(beacons) for neigh in neighs
    ])
    bearings_to_neighs = np.arctan2(bearing_vecs_to_neighs[:, 1], bearing_vecs_to_neighs[:, 0])
    nominal_heading = Min.get_exploration_dir(bearings_to_neighs, num_neighs_of_neighs)
    nominal_heading_vec = p2v(1, nominal_heading)

    """ Plotting decision""" 
    if mn.ID in show_decisions_for:
      _, dec_ax = plt.subplots()
      env.plot(dec_ax)
      mn.plot(dec_ax)
      dec_ax.set_title(f"{mn.ID} deciding direction")

      for i in np.arange(len(neighs)):
        print(f"Neighbor ID: {neighs[i].ID}, num_neighs: {num_neighs_of_neighs[i]}")
        plot_vec(dec_ax, bearing_vecs_to_neighs[i], mn.pos, clr="red" if neighs[i].get_num_neighbors(beacons) >= 3 else "yellow")
        neighs[i].plot(dec_ax)

      plot_vec(dec_ax, nominal_heading_vec, mn.pos, "pink", alpha=0.4)
      plt.show()
    """"""
    cnt = 0
    while mn.state == MinState.EXPLORING and cnt < 5000:
      cnt += 1
      if cnt == 5000:
        print(f"OVERFLOW for min {mn.ID}")
      obs_vec = mn.get_obstacle_avoidance_heading(env)
      mn.set_heading_and_speed(nominal_heading_vec, obs_vec, speed=1)

      RSSI_ok = np.array([mn.get_RSSI(b) > np.exp(-2.6) for b in beacons])
      if np.count_nonzero(RSSI_ok) == 0:
        mn.state = MinState.LANDED
        beacons.append(mn)
      else: mn.do_step(dt)
    
    print(f"min {mn.ID} landed at pos\t\t\t {mn.pos}\n------------------", )
  return mins

if __name__ == "__main__":
  _animate, save_animation = False, False
  start_animation_from_min_ID = 0


  env = Env(np.array([
    [-10, -10],
    [ 10, -10],
    [ 10,  10],
    [-10,  10]
  ]), np.array([
    -9.8, -9.8
  ]))

  max_range = 3


  N_mins = 13
  dt = 0.01

  SCS = Beacon(max_range)
  mins = [Min(max_range) for i in range(N_mins)]
  mins = simulate(dt, mins, SCS, env, show_decisions_for=[13])

  fig, ax = plt.subplots(1)

  ax.set_xlim([
    np.min(np.concatenate([mn.pos_traj[0, :] for mn in mins])) - max_range, 
    np.max(np.concatenate([mn.pos_traj[0, :] for mn in mins])) + max_range
  ])
  ax.set_ylim([
    np.min(np.concatenate([mn.pos_traj[1, :] for mn in mins])) - max_range,
    np.max(np.concatenate([mn.pos_traj[1, :] for mn in mins])) + max_range
  ])


  
  if _animate:
    offset, min_counter = [0], [start_animation_from_min_ID]
    print(f"total frames: {np.sum([mn.pos_traj.shape[1] for mn in mins])}")

    def init():
      SCS.plot(ax)
      env.plot(ax)
      artists = []
      for mn in mins:
        artists += mn.plot(ax)
        artists += (mn.plot_traj_line(ax), )
        mn.plot_pos_from_pos_traj_index(0)
      return artists

    def animate(i, ax):
      if i - offset[0] >= mins[min_counter[0]].pos_traj.shape[1]:
        offset[0] += mins[min_counter[0]].pos_traj.shape[1]
        min_counter[0] += 1

      return mins[min_counter[0]].plot_pos_from_pos_traj_index(i - offset[0])



    anim = FuncAnimation(fig, animate, fargs=(ax, ), init_func=init, frames=np.sum([mn.pos_traj.shape[1] for mn in mins]), interval=2, blit=False)
    if save_animation:
      animation_name = "animation.gif"
      print("Saving animation")
      anim.save(animation_name)
      print(f"Animation saved to {animation_name}")
    else:
      plt.show()
  
  else:
    env.plot(ax)
    SCS.plot(ax)
    for mn in mins:
      mn.plot(ax)
      mn.plot_traj_line(ax)
    import sys
    """ Plotting Fisher determinant value
    sys.path.append('./')
    from fisher_determinant_approach import plot_color_map as pcm
    S = np.hstack([SCS.pos.reshape(2, 1)] + [mn.pos.reshape(2, 1) for mn in mins])
    pcm(fig, ax, 1000, [-10, 10], [-10, 10], S, 1)
    """
    plt.show()
