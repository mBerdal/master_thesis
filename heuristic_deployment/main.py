from environment import Env
from beacon import Beacon
from min import Min, MinState
from helpers import polar_to_vec as p2v

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate(dt, mins, SCS, env):
  SCS.insert_into_environment(env)
  beacons = [SCS]

  for mn in mins:
    mn.insert_into_environment(env)

    mn.state = MinState.FOLLOWING
    heading = mn.get_bearing_to_other(beacons[-1])
    mn.set_heading_and_speed(heading, 1)
    while mn.state == MinState.FOLLOWING:
      if mn.is_within_circle_of_acceptance(beacons[-1]):
        mn.state = MinState.EXPLORING
      else: mn.do_step(dt)
    
    print(f"min {mn.ID} stopped following at pos\t\t", mn.pos)
    neighs = mn.get_neighbors(beacons)
    bearings_to_neighs = np.array([
      mn.get_bearing_to_other(neigh) for neigh in neighs
    ])
    num_neighs_of_neighs = np.array([
      neigh.get_num_neighbors(beacons) for neigh in neighs
    ])
    nominal_heading = Min.get_exploration_dir(bearings_to_neighs, num_neighs_of_neighs)
    nominal_heading_vec = p2v(1, nominal_heading)

    mn.set_heading_and_speed(nominal_heading, 1)

    while mn.state == MinState.EXPLORING:
      """ Obstacle avoidance part 
      xtra_heading_vec = np.zeros((2, ))
      for s in mn.sensors:
        r = s.sense(env).get_val()
        abs_ang = nominal_heading + s.host_relative_angle
        if mn.ID == 3:
          print(p2v(-1/r, abs_ang), np.rad2deg(s.host_relative_angle))
        xtra_heading_vec += p2v(-1/r, abs_ang)
      total_heading_vec = nominal_heading_vec + xtra_heading_vec
      total_heading = np.arctan2(total_heading_vec[1], np.rad2deg(total_heading_vec[0]))
      if mn.ID == 3:
        print(np.rad2deg(mn.heading), np.rad2deg(nominal_heading), xtra_heading_vec, np.rad2deg(total_heading))
      mn.set_heading_and_speed(total_heading, 1)
      """
      RSSI_ok = np.array([mn.get_RSSI(neigh) > np.exp(-2.6) for neigh in neighs])
      if np.count_nonzero(RSSI_ok) == 0:
        mn.state = MinState.LANDED
        beacons.append(mn)
      else: mn.do_step(dt)
    
    print(f"min {mn.ID} landed at pos\t\t\t {mn.pos}\n------------------", )
  return mins

if __name__ == "__main__":
  _animate, save_animation = True, False


  env = Env(np.array([
    [-10, -10],
    [ 10, -10],
    [ 10,  10],
    [-10,  10]
  ]), np.array([
    -9.8, -9.8
  ]))

  max_range = 3


  N_mins = 10
  dt = 0.01

  SCS = Beacon(max_range)
  mins = [Min(max_range) for i in range(N_mins)]
  mins = simulate(dt, mins, SCS, env)

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
    offset, min_counter = [0], [0]

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
    plt.show()
