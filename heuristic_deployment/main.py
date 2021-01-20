from environment import Env
from beacon import Beacon
from min import Min, MinState

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


if __name__ == "__main__":

  E = Env(np.array([
    [-1, -1],
    [ 1, -1],
    [ 1,  1],
    [-1,  1]
  ]), np.array([
    -0.8, -0.8
  ]))

  N_mins = 10
  max_range = 3

  beacons = [Beacon(max_range, E.entrance_point)]
  beacons[0].insert_into_environment(E)
  sampling_time = 0.01

  N_mins = 2

  beacons = [Beacon(3)]
  beacons[0].insert_into_environment(E)
  sampling_time = 0.01

  for i in range(N_mins):
    mn = Min(3)
    mn.insert_into_environment(E)

    mn.state = MinState.FOLLOWING
    heading = beacons[-1].get_bearing_to_other(mn)
    mn.set_heading_and_speed(heading, 1)
    while mn.state == MinState.FOLLOWING:
      if mn.is_within_circle_of_acceptance(beacons[-1]):
        mn.state = MinState.EXPLORING
      else: mn.do_step(sampling_time)
    
    print(f"min {i} stopped following at pos ", mn.pos)

    while mn.state == MinState.EXPLORING:
      neighs = mn.get_neighbors(beacons)
      bearings_to_neighs = np.array([
        mn.get_bearing_to_other(neigh) for neigh in neighs
      ])
      num_neighs_of_neighs = np.array([
        neigh.get_num_neighbors(beacons) for neigh in neighs
      ])
      heading = Min.get_exploration_dir(bearings_to_neighs, num_neighs_of_neighs)
      mn.set_heading_and_speed(heading, 1)
      RSSI_ok = np.array([mn.get_RSSI(neigh) > np.exp(-2.6) for neigh in neighs])
      if np.count_nonzero(RSSI_ok) == 0:
        mn.state = MinState.LANDED
        beacons.append(mn)
      else: mn.do_step(sampling_time)
    
    print(f"min {i} landed at pos ", mn.pos)

  fig, ax = plt.subplots(1)

  ax.set_xlim([
    np.min(np.concatenate([b.pos_traj[0, :] for b in beacons])) - max_range, 
    np.max(np.concatenate([b.pos_traj[0, :] for b in beacons])) + max_range
  ])
  ax.set_ylim([
    np.min(np.concatenate([b.pos_traj[1, :] for b in beacons])) - max_range,
    np.max(np.concatenate([b.pos_traj[1, :] for b in beacons])) + max_range
  ])

  offset, min_counter = [0], [1]

  beacons[0].plot(ax)

  for b in beacons:
    print(f"min {b.ID} converged in {b.pos_traj.shape[1]-1} steps")

  def animate_aux(i, min_index, offset, ax):
    return beacons[min_index].plot_pos_from_pos_traj_index(i - offset)

  def init():
    shapes = beacons[0].plot(ax)
    for b in beacons[1:]:
      shapes += b.plot(ax)
      shapes += (b.plot_traj_line(ax), )
      b.plot_pos_from_pos_traj_index(0)
    return shapes

  def animate(i, ax):
    if i - offset[0] >= beacons[min_counter[0]].pos_traj.shape[1]:
      offset[0] += beacons[min_counter[0]].pos_traj.shape[1]
      min_counter[0] += 1
    return animate_aux(i, min_counter[0], offset[0], ax)

anim = FuncAnimation(fig, animate, fargs=(ax, ), init_func=init, frames=np.sum([b.pos_traj.shape[1] for b in beacons[1:]]), interval=20, blit=True)
#anim.save("a.gif", writer="Pillow")
