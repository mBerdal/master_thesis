from environment import Env

from beacons.SCS.scs import SCS
from beacons.MIN.min import Min, MinState

from helpers import (
  rot_mat_2D,
  normalize,
  plot_configuration,
  animate_configuration,
  plot_speed_trajs,
  plot_gains
)

from line_deployment import LineDeployment

from plot_fields import FieldPlotter

import numpy as np
import matplotlib.pyplot as plt


def simulate(dt, mins, scs, env):
  scs.insert_into_environment(env)
  beacons = np.array([scs], dtype=object)
  t = 0
  for m in mins:
    m.insert_into_environment(beacons, env, t)
    while not m.state == MinState.LANDED:
          m.do_step(beacons, scs, env, dt)
          t += dt
    beacons = np.append(beacons, m)
    print(f"min {m.ID} landed at pos\t\t\t {m.pos}")

  return beacons

if __name__ == "__main__":

  animate, save_anim_or_img = False, True
  fig_name = None

  env = Env(
    np.array([
      0, 0
    ]),
    obstacle_corners = [
      
    ]
  )
  """
  np.array([
        [-1, -1],
        [5, -1],
        [5, 5],
        [-1, 5]
      ])
  """

  N_mins = 10
  dt = 10e-3

  XI_BAR = 3
  TAU_XI = 0.5
  D_BAR = 5

  scs = SCS(xi_max=XI_BAR, d_perf=1, d_none=3)

  """ Line exploration """
  def tmp(MIN, neighs, F_O):
    v_neighs = np.sum(np.hstack([(MIN.pos - n.pos).reshape(2, 1) for n in neighs]), axis=1).reshape(2, 1)
    xtra_angle = 1*np.pi/2*(-1)**(MIN.ID-1)
    return normalize(rot_mat_2D(xtra_angle)@v_neighs)

  sensor_range = 1
  mins = [
    Min(
      sensor_range,
      LineDeployment(d_bar=D_BAR, xi_bar=XI_BAR, tau_xi=TAU_XI, field_type=2, get_exploration_dir_callback=lambda MIN, neighs, F_o: tmp(MIN, neighs, F_o)),
      xi_max=XI_BAR,
      d_perf=1,
      d_none=3
    ) for _ in range(N_mins)
  ]


  beacons = simulate(dt, mins, scs, env)
  #F = FieldPlotter(beacons=beacons, RSSI_threshold=LineExplore.RSSI_TRHESHOLD, save_to_file_prefix=fig_name)
  #F.plot_potential_field()
  #F.plot_force_field()


  plot_speed_trajs(mins, fig_name)
  plot_gains(beacons, fig_name)

  if animate:
    animate_configuration(env, scs, mins, fig_name)
  else:
    plot_configuration(env, scs, mins, fig_name)
  plt.show()

