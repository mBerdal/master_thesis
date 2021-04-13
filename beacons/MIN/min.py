from beacons.beacon import Beacon
from beacons.MIN.range_sensor import RangeSensor
from helpers import (
  get_smallest_signed_angle as ssa,
  get_vector_angle as gva,
  polar_to_vec as p2v,
  euler_int,
  plot_vec,
  rot_z_mat as R_z
)
from deployment_helpers import AtLandingConditionException

import numpy as np
from enum import Enum

class MinState(Enum):
  ACTIVE   = 0,
  LANDED   = 1

class Min(Beacon):
      
  def __init__(self, sensor_range, deployment_strategy, xi_max, d_perf, d_none, k=0, a=0, exploration_dir=np.zeros((2, )), turning_time_constant = 0.5):
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
    self._pos_traj = self.pos.reshape(2, 1)
    self._heading_traj = np.array([self.heading])
    self.__speed_traj = np.zeros(1, )
    self.__timeline = start_time*np.ones(1, )

  def do_step(self, beacons, SCS, ENV, dt):
    try:
      v = self.deployment_strategy.get_velocity_vector()
      self.__speed_traj = np.append(self.__speed_traj, np.linalg.norm(v))
      self.__timeline = np.append(self.__timeline, self.__timeline[-1] + dt)

      self.pos = euler_int(self.pos, v, dt)
      psi_ref = gva(v)
      self.heading = euler_int(self.heading, (1/self.turning_time_constant)*(ssa(psi_ref - self.heading)), dt)
      self._pos_traj = np.hstack((self._pos_traj, self.pos.reshape(2, 1)))
      self._heading_traj = np.concatenate((self._heading_traj, [self.heading]))
    except AtLandingConditionException:
      self.state = MinState.LANDED
  
  def get_timeline(self):
        return self.__timeline
  
  def get_speed_traj(self):
        return self.__speed_traj

  def get_neighs(self):
        assert self.state == MinState.LANDED, "Neighbors are not defined until MIN has landed"
        return self.deployment_strategy.neighs

  def get_list_of_measured_ranges_and_angs_rel_x_axis(self):
        obs_ranges_and_angles = list()
        for s in self.sensors:
            s.sense(self.environment)
            if s.measurement.get_range() < self.sensor_range:
                  obs_ranges_and_angles.append((s.measurement.get_range(), self.heading + s.host_relative_angle))
        return obs_ranges_and_angles
  
  def get_total_obstacle_vector(self):
        vec = np.zeros((2, ))
        for s in self.sensors:
              s.sense(self.environment)
              vec += p2v(s.measurement.get_range(), self.heading + s.host_relative_angle)
        return vec

  """""
  PLOTTING STUFF
  """""
  def plot(self, axis):
    self.heading_arrow = plot_vec(axis, p2v(1, self.heading), self.pos)
    return super().plot(axis) + (self.heading_arrow, )

  def plot_traj_line(self, axis):
    self.traj_line, = axis.plot(*self._pos_traj, alpha=0.4)
    return self.traj_line

  def plot_pos_from_pos_traj_index(self, index):
    new_pos = self._pos_traj[:, index]
    self.point.set_data(new_pos)
    self.annotation.set_x(new_pos[0])
    self.annotation.set_y(new_pos[1])
    self.traj_line.set_data(self._pos_traj[:, :index])

    self.heading_arrow.set_data(*np.hstack((new_pos.reshape(2, 1), new_pos.reshape(2, 1) + p2v(1, self._heading_traj[index]).reshape(2, 1))))
    return self.point, self.annotation, self.traj_line, self.heading_arrow