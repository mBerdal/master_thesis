from environment import Env
from beacon import Beacon
from min import Min, MinState
from helpers import polar_to_vec as p2v, plot_vec, get_vector_angle as gva, normalize

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate(dt, mins, SCS, env, k, show_decisions_for = []):
  SCS.insert_into_environment(env)
  beacons = np.array([SCS], dtype=object)

  for mn in mins:
    mn.insert_into_environment(env)
    print(f"min {mn.ID} taking off")
    mn.state = MinState.FOLLOWING

    target = beacons[-1]
    print(f"min {mn.ID} targeting beacon {target.ID}")

    mn.set_heading_and_speed(gva(mn.get_vec_to_other(target)), speed=2)
    while mn.state == MinState.FOLLOWING:
      if mn.get_RSSI(target) > np.exp(-0.2):
        mn.state = MinState.EXPLORING
      else: mn.do_step(dt)

    prev_neigh_IDS = set()
    while mn.state == MinState.EXPLORING:
      mn.compute_neighbors(beacons)
      curr_neigh_IDs = set(n.ID for n in mn.neighbors)

      if curr_neigh_IDs.isdisjoint(prev_neigh_IDS):
        exploration_dir = mn.get_exploration_dir(3)
        exploration_vec = p2v(1, exploration_dir)
        prev_neigh_IDS = curr_neigh_IDs
        
      obs_vec = mn.get_obstacle_avoidance_vec(env)
      mn.set_heading_and_speed(gva(exploration_vec + obs_vec), speed=1)

      RSSI_ok = np.array([mn.get_RSSI(b) > np.exp(-2.6) for b in beacons])
      
      if np.abs(exploration_dir - gva(exploration_vec + obs_vec)) > np.pi/2 or np.count_nonzero(RSSI_ok) == 0:
        mn.state = MinState.LANDED
      else: mn.do_step(dt)

    beacons = np.append(beacons, mn)
    for b in beacons:
      b.compute_neighbors(beacons)
    print(f"min {mn.ID} landed at pos\t\t\t {mn.pos}\n------------------", )
  return mins

if __name__ == "__main__":
  _animate, save_animation = True, False
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


  N_mins = 9
  dt = 0.01

  SCS = Beacon(max_range)
  mins = [Min(max_range) for i in range(N_mins)]
  mins = simulate(dt, mins, SCS, env, k=3, show_decisions_for=[])

  fig, ax = plt.subplots(1)

  
  if _animate:
    offset, min_counter = [0], [start_animation_from_min_ID]

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
      if i - offset[0] >= mins[min_counter[0]].get_pos_traj_length():
        offset[0] += mins[min_counter[0]].get_pos_traj_length()
        min_counter[0] += 1

      return mins[min_counter[0]].plot_pos_from_pos_traj_index(i - offset[0])



    anim = FuncAnimation(fig, animate, fargs=(ax, ), init_func=init, interval=2, blit=False)
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
