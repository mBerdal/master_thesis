from environment import Env

from beacons.SCS.scs import SCS
from beacons.MIN.min import Min, MinState

from deployment.following_strategies.attractive_follow import AttractiveFollow
from deployment.following_strategies.straight_line_follow import StraightLineFollow
from deployment.exploration_strategies.potential_fields_explore import PotentialFieldsExplore
from deployment.exploration_strategies.heuristic_explore import HeuristicExplore
from deployment.following_strategies.no_follow import NoFollow
from deployment.exploration_strategies.line_explore import (
  LineExplore,
  LineExploreKind
)
from deployment.deployment_fsm import DeploymentFSM

from plot_fields import FieldPlotter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate(dt, mins, scs, env):
  scs.insert_into_environment(env)
  beacons = np.array([scs], dtype=object)

  dists_to_prev = np.zeros((len(mins)))
  dists_bar = np.zeros(len(mins))

  for m in mins:
    m.insert_into_environment(env)
    while not m.state == MinState.LANDED:
          m.do_step(beacons, scs, env, dt)
    beacons = np.append(beacons, m)
    for b in beacons:
      b.compute_neighbors(beacons)
    print(f"min {m.ID} landed at pos\t\t\t {m.pos}")


    dists_to_prev[m.ID - 1] = np.linalg.norm(beacons[-1].pos - beacons[-2].pos)
    dists_bar[m.ID - 1] = np.sum(dists_to_prev)/(len(beacons) - 1)

    if not m.deployment_strategy.get_target() is None:
          print(f"Its target now has {len(m.deployment_strategy.get_target().neighbors)} neighs\n------------------", )
  print(f"minimum number of neighbors: {min(beacons, key=lambda b: len(b.neighbors))}")

  print("D")
  print(dists_to_prev)
  print("D_bar")
  print(dists_bar)
  print("---")
  return beacons

if __name__ == "__main__":

  _animate, save_anim_or_img = False, False
  anim_or_fig_name = "fig"
  start_animation_from_min_ID = 0

  env = Env(
    np.array([
      0, 0
    ]),
    obstacle_corners = []
  )

  max_range = 3

  N_mins = 7
  dt = 10e-4

  scs = SCS(max_range)

  """ Line exploration """

  mins = [
    Min(
      max_range,
      DeploymentFSM(
        NoFollow(),
        LineExplore(
          K_o=0.01,
          kind=LineExploreKind.TWO_DIM_LOCAL,
        )
      ),
      xi_max=3,
      d_perf=1,
      d_none=3
    ) for _ in range(N_mins)
  ]


  beacons = simulate(dt, mins, scs, env)

  F = FieldPlotter(beacons=beacons, RSSI_threshold=LineExplore.RSSI_TRHESHOLD)
  F.plot_potential_field()
  F.plot_force_field()

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

    def animate(i):
      if i - offset[0] >= mins[min_counter[0]].get_pos_traj_length():
        offset[0] += mins[min_counter[0]].get_pos_traj_length()
        min_counter[0] += 1

      return mins[min_counter[0]].plot_pos_from_pos_traj_index(i - offset[0])



    anim = FuncAnimation(fig, animate, init_func=init, interval=2, blit=False)
    if save_anim_or_img:
      animation_name = anim_or_fig_name + ".gif"
      print("Saving animation")
      anim.save(animation_name)
      print(f"Animation saved to {animation_name}")

  else:
    env.plot(ax)
    scs.plot(ax)
    for mn in mins:
      mn.plot(ax)
      mn.plot_traj_line(ax)
    fig.savefig(anim_or_fig_name + ".png", bbox_inches="tight")
  plt.show()

