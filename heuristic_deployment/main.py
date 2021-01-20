from environment import Env
from beacon import Beacon
from min import Min, MinState

import numpy as np
import matplotlib.pyplot as plt
from time import sleep


if __name__ == "__main__":

  E = Env(np.array([
    [-1, -1],
    [ 1, -1],
    [ 1,  1],
    [-1,  1]
  ]), np.array([
    -0.8, -0.8
  ]))

  N_mins = 100

  beacons = [Beacon(3, E.entrance_point)]
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
  for b in beacons:
    b.plot(ax)
    print(b)
  plt.show()
