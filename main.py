from environment import Env

from beacons.SCS.scs import SCS
from beacons.MIN.min import Min, MinState

from helpers import (
    rot_mat_2D,
    normalize,
    plot_configuration,
    animate_configuration,
    plot_speed_trajs,
    plot_gains,
    generalized_sample_variance,
    total_sample_variance,
    plot_vec
)

from line_deployment import LineDeployment

from plot_fields import FieldPlotter
  
import numpy as np
import matplotlib.pyplot as plt


def simulate(dt, mins, scs, env, max_min_iter=3000):
    scs.insert_into_environment(env)
    beacons = np.array([scs], dtype=object)
    prev_min_landing_time = 0
    for m in mins:
        num_steps_taken = 0
        m.insert_into_environment(beacons, env, prev_min_landing_time)
        while not m.state == MinState.LANDED:
            m.do_step(beacons, scs, env, dt)
            num_steps_taken += 1
            if num_steps_taken > max_min_iter:
                print(f"MIN {m.ID} stopped due to too many steps")
                beacons = np.append(beacons, m)
                return beacons

        prev_min_landing_time = m.get_landing_time()
        beacons = np.append(beacons, m)
        print(f"min {m.ID} landed at pos\t\t\t {m.pos}")
    return beacons

""" Exploration direction """
def get_exploration_dir(MIN, neighs, obs_vec):
    v_neighs = normalize(np.sum(np.hstack(
        [(MIN.pos - n.pos).reshape(2, 1) for n in neighs]), axis=1).reshape(2, 1))

    xtra_angle = 0.5 * np.pi/2 * np.random.uniform(-1, 1)
    tmp = (rot_mat_2D(xtra_angle)@v_neighs).reshape(2, )
    if obs_vec is None: 
        print("NO OBSTACLES")
        return tmp

    neighs.discard(scs)
    ax = plot_configuration(env, scs, [MIN] + list(neighs))
    k = np.linalg.norm(obs_vec)/MIN.sensor_range
    v = normalize((k*tmp + (1-k)*normalize(-obs_vec)))

    plot_vec(ax, -obs_vec, MIN.pos, clr="red")
    plot_vec(ax, tmp, MIN.pos, clr="green")
    plot_vec(ax, v, MIN.pos, clr="yellow")
    print(np.linalg.norm(obs_vec), MIN.sensor_range, k)
    plt.show()
    return v


if __name__ == "__main__":
    N_mins = 10

    animate = False
    fig_name = f"{N_mins}_agnt_rectangular_room_k_gain_try3"

    env = Env(
        np.array([
            0, 0
        ]),
        obstacle_corners=[
             np.array([
                [-1, -1],
                [10, -1],
                [10, 10],
                [-1, 10],
            ])
        ]
    )

    dt = 10e-3

    XI_BAR = 3
    TAU_XI = 0.5
    D_BAR = 5

    sensor_range = 2

    scs = SCS(xi_max=XI_BAR, d_perf=1, d_none=3)

    mins = [
        Min(
            sensor_range,
            LineDeployment(d_bar=D_BAR, xi_bar=XI_BAR, tau_xi=TAU_XI, field_type=1,
                           get_exploration_dir_callback=lambda MIN, neighs, F_o: get_exploration_dir(MIN, neighs, F_o)),
            xi_max=XI_BAR,
            d_perf=1,
            d_none=3
        ) for _ in range(N_mins)
    ]
    beacons = simulate(dt, mins, scs, env)

    #F = FieldPlotter(beacons=beacons, RSSI_threshold=XI_BAR, save_to_file_prefix=fig_name)
    # F.plot_potential_field()
    # F.plot_force_field()

    variance_measures = np.zeros((2, len(beacons)))
    for i in range(2, len(beacons) + 1):
        beacon_positions = np.concatenate(
            [b.pos.reshape(2, 1) for b in beacons[:i]], axis=1)
        variance_measures[0, i -
                          1] = generalized_sample_variance(beacon_positions)
        variance_measures[1, i-1] = total_sample_variance(beacon_positions)

    fig, ax = plt.subplots()
    ax.plot(np.arange(0, len(beacons)),
            variance_measures[0, :], label="Generalized variance")
    ax.plot(np.arange(0, len(beacons)),
            variance_measures[1, :], label="Total variance")
    ax.legend()

    plot_speed_trajs(mins, fig_name)
    plot_gains(beacons, fig_name)

    if animate:
        animate_configuration(env, scs, mins, fig_name)
    else:
        plot_configuration(env, scs, mins, fig_name)
    plt.show()
