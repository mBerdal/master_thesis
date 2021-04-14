from beacons.beacon import Beacon
from beacons.MIN.range_sensor import RangeSensor
from helpers import (
    get_smallest_signed_angle as ssa,
    get_vector_angle as gva,
    polar_to_vec as p2v,
    euler_int,
    plot_vec,
    rot_z_mat as R_z,
    FastExpandableNpArray as FastArray
)
from deployment_helpers import AtLandingConditionException

import numpy as np
from enum import Enum


class MinState(Enum):
    ACTIVE = 0,
    LANDED = 1


class Min(Beacon):
    NUM_DATA_POINTS = 6
    POS_X_DATA_IDX = 0
    POS_Y_DATA_IDX = 1
    VEL_X_DATA_IDX = 2
    VEL_Y_DATA_IDX = 3
    HEADING_DATA_IDX = 4
    TIME_DATA_IDX = 5

    def __init__(self, sensor_range, deployment_strategy, xi_max, d_perf, d_none, k=0, a=0, exploration_dir=np.zeros((2, )), turning_time_constant=0.5):
        super().__init__(xi_max, d_perf, d_none, k, a, exploration_dir)
        self.deployment_strategy = deployment_strategy
        self.turning_time_constant = turning_time_constant
        self.sensor_range = sensor_range
        self.sensors = list()
        for ang in np.arange(0, 360, 90):
            r = RangeSensor(sensor_range)
            r.mount(self, ang)

    def insert_into_environment(self, beacons, env, start_time):
        super().insert_into_environment(env)
        self.deployment_strategy.init_deployment(self, beacons, env)
        self.state = MinState.ACTIVE
        self.heading = 0

        self.__data_traj = FastArray(self.NUM_DATA_POINTS)
        self.__data_traj.append([
            self.pos[0],
            self.pos[1],
            0,
            0,
            self.heading,
            start_time
        ])

    def do_step(self, beacons, SCS, ENV, dt):
        try:
            v = self.deployment_strategy.get_velocity_vector()
            self.pos = euler_int(self.pos, v, dt)
            psi_ref = gva(v)
            self.heading = euler_int(
                self.heading, (1/self.turning_time_constant)*(ssa(psi_ref - self.heading)), dt)
            self.__store_step_data(v, dt)
        except AtLandingConditionException:
            self.state = MinState.LANDED

    def __store_step_data(self, v, dt):
        self.__data_traj.append([
            self.pos[0],
            self.pos[1],
            v[0],
            v[1],
            self.heading,
            self.__data_traj.get_val(self.TIME_DATA_IDX, -1) + dt
        ])


    def get_pos_traj(self):
        return self.__data_traj.get()[[self.POS_X_DATA_IDX, self.POS_Y_DATA_IDX], :]

    def get_vel_traj(self):
        return self.__data_traj.get()[[self.VEL_X_DATA_IDX, self.VEL_Y_DATA_IDX], :]

    def get_speed_traj(self):
        return np.linalg.norm(self.get_vel_traj(), axis=0)
    
    def get_heading_traj(self):
        return self.__data_traj.get()[self.HEADING_DATA_IDX, :]

    def get_timeline(self):
        return self.__data_traj.get()[self.TIME_DATA_IDX, :]

    def get_landing_time(self):
        assert self.state == MinState.LANDED, "landing time is not valid until the MIN has landed"
        return self.__data_traj.get_val(self.TIME_DATA_IDX, -1)

    def get_neighs(self):
        assert self.state == MinState.LANDED, "Neighbors are not defined until MIN has landed"
        return self.deployment_strategy.neighs

    def get_list_of_measured_ranges_and_angs_rel_x_axis(self):
        obs_ranges_and_angles = list()
        for s in self.sensors:
            r, ang_rel_x_axis = s.get_measurement(self.environment)
            if r < self.sensor_range:
                obs_ranges_and_angles.append((r, ang_rel_x_axis))
        return obs_ranges_and_angles

    def get_total_obstacle_vector(self):
        vec = np.zeros((2, ))
        for s in self.sensors:
            r, ang_rel_x_axis = s.get_measurement(self.environment)
            vec += p2v(r, ang_rel_x_axis)
        return vec

    """""
  PLOTTING STUFF
  """""

    def plot(self, axis):
        self.heading_arrow = plot_vec(axis, p2v(1, self.heading), self.pos)
        return super().plot(axis) + (self.heading_arrow, )

    def plot_traj_line(self, axis):
        self.traj_line, = axis.plot(
            *self.__data_traj.get()[[self.POS_X_DATA_IDX, self.POS_Y_DATA_IDX], :], alpha=0.4)
        return self.traj_line

    def plot_pos_from_pos_traj_index(self, index):
        data_traj = self.__data_traj.get()
        new_pos = data_traj[[self.POS_X_DATA_IDX, self.POS_Y_DATA_IDX], index]

        self.point.set_data(new_pos)
        self.annotation.set_x(new_pos[0])
        self.annotation.set_y(new_pos[1])
        self.traj_line.set_data(
            data_traj[[self.POS_X_DATA_IDX, self.POS_Y_DATA_IDX], :index])

        self.heading_arrow.set_data(*np.hstack((new_pos.reshape(2, 1), new_pos.reshape(
            2, 1) + p2v(1, data_traj[self.HEADING_DATA_IDX, index]).reshape(2, 1))))
        return self.point, self.annotation, self.traj_line, self.heading_arrow
