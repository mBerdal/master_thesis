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
from deployment.exploration_strategies.two_dim_local_line_explore import TWO_DIM_LOCAL_LINE_EXPLORE
from deployment.deployment_fsm import DeploymentFSM
from helpers import rot_mat_2D, normalize, plot_configuration, animate_configuration, plot_speed_trajs

from plot_fields import FieldPlotter

import numpy as np
import matplotlib.pyplot as plt


def simulate(dt, mins, scs, env):
  scs.insert_into_environment(env)
  beacons = np.array([scs], dtype=object)
  t = 0
  for m in mins:
    m.insert_into_environment(env, t)
    if isinstance(m.deployment_strategy.es, TWO_DIM_LOCAL_LINE_EXPLORE):
        m.deployment_strategy.es.load_beacon_info(beacons)
    
    while not m.state == MinState.LANDED:
          m.do_step(beacons, scs, env, dt)
          t += dt
    beacons = np.append(beacons, m)
    print(f"min {m.ID} landed at pos\t\t\t {m.pos}")

    if not m.deployment_strategy.get_target() is None:
          print(f"Its target now has {len(m.deployment_strategy.get_target().neighbors)} neighs\n------------------", )
  return beacons

if __name__ == "__main__":

  animate, save_anim_or_img = False, True
  fig_name = "dynamic_gain_setting_15_mins_avg_neigh_explore"

  env = Env(
    np.array([
      0, 0
    ]),
    obstacle_corners = [
      np.array([
        [-1, -1],
        [5, -1],
        [5, 5],
        [-1, 5]
      ])
    ]
  )
  """

  """

  N_mins = 10
  dt = 10e-4

  scs = SCS(xi_max=3, d_perf=1, d_none=3)

  """ Line exploration """
  def tmp(MIN, neighs, F_O):
    v_neighs = np.sum(np.hstack([(MIN.pos - n.pos).reshape(2, 1) for n in neighs]), axis=1).reshape(2, 1)
    print(MIN.ID, " landed with neighs ", [n.ID for n in neighs])
    xtra_angle = ((-1)**(MIN.ID-1))*np.pi/2
    return normalize(rot_mat_2D(xtra_angle)@v_neighs)

  sensor_range = 1
  mins = [
    Min(
      sensor_range,
      DeploymentFSM(
        NoFollow(),
        TWO_DIM_LOCAL_LINE_EXPLORE(
          K_o=0.01,
          get_exploration_dir_callback=lambda MIN, neighs, F_O: tmp(MIN, neighs, F_O)
        )
      ),
      xi_max=3,
      d_perf=1,
      d_none=3
    ) for _ in range(N_mins)
  ]


  beacons = simulate(dt, mins, scs, env)
  #F = FieldPlotter(beacons=beacons, RSSI_threshold=LineExplore.RSSI_TRHESHOLD, save_to_file_prefix=fig_name)
  #F.plot_potential_field()
  #F.plot_force_field()


  plot_speed_trajs(mins, fig_name)

  if animate:
    animate_configuration(env, scs, mins, fig_name)
  else:
    plot_configuration(env, scs, mins, fig_name)
  plt.show()

