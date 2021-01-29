from environment import Env
from scs import SCS
from min import Min, MinState
from deployment_strategies.heuristic_deploy import HeuristicDeploy
from deployment_strategies.potential_fields_deploy import PotentialFieldsDeploy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate(dt, MINs, SCS, env):
  SCS.insert_into_environment(env)
  beacons = np.array([SCS], dtype=object)

  for mn in MINs:
    mn.insert_into_environment(env)
    while not mn.state == MinState.LANDED:
          mn.do_step(beacons, SCS, env, dt)

    beacons = np.append(beacons, mn)
    for b in beacons:
      b.compute_neighbors(beacons)
    print(f"min {mn.ID} landed at pos\t\t\t {mn.pos}\n------------------", )

if __name__ == "__main__":

  _animate, save_animation = False, False
  start_animation_from_min_ID = 0

  env = Env(
    np.array([
      -9.8, -9.8
    ]),
    obstacle_corners = [
    np.array([
      [-10, -10],
      [ 10, -10], 
      [ 10,  10],
      [-10,  10]
    ])
    ]
  )


  max_range = 3

  N_mins = 10
  dt = 0.01

  scs = SCS(max_range)
  mins = [Min(max_range, PotentialFieldsDeploy()) for i in range(N_mins)]
  
  simulate(dt, mins, scs, env)

  fig, ax = plt.subplots(1)

  
  if _animate:
    offset, min_counter = [0], [start_animation_from_min_ID]

    def init():
      scs.plot(ax)
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
    scs.plot(ax)
    for mn in mins:
      mn.plot(ax)
      mn.plot_traj_line(ax)

    """ Plotting Fisher determinant value
    import sys
    sys.path.append('./')
    from fisher_determinant_approach import plot_color_map as pcm
    S = np.hstack([scs.pos.reshape(2, 1)] + [mn.pos.reshape(2, 1) for mn in mins])
    pcm(fig, ax, 1000, [-10, 10], [-10, 10], S, 1)
    """ 
    plt.show()
