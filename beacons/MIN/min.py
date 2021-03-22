from beacons.beacon import Beacon
from beacons.MIN.range_sensor import RangeSensor
from helpers import (
  get_smallest_signed_angle as ssa,
  get_vector_angle as gva,
  polar_to_vec as p2v,
  euler_int,
  plot_vec
)

import numpy as np
from enum import Enum

class MinState(Enum):
  SPAWNED   = 0,
  FOLLOWING = 1,
  EXPLORING = 2,
  LANDED    = 3

class Min(Beacon):
      
  clr = {
    MinState.SPAWNED:   "yellow",
    MinState.FOLLOWING: "red",
    MinState.EXPLORING: "green",
    MinState.LANDED:    "black",
  }

  def __init__(self, sensor_range, deployment_strategy, xi_max, d_perf, d_none, k=0, a=0, exploration_dir=np.zeros((2, ))):
    super().__init__(xi_max, d_perf, d_none, k, a, exploration_dir)
    self.deployment_strategy = deployment_strategy
    self.sensors = []
    for ang in np.arange(0, 360, 90):
      r = RangeSensor(sensor_range)
      r.mount(self, ang)

  def insert_into_environment(self, env, start_time):
    super().insert_into_environment(env)
    self.state = MinState.SPAWNED
    self.heading = 0
    self.state_traj = np.array([self.state], dtype=object)
    self._pos_traj = self.pos.reshape(2, 1)
    self._heading_traj = np.array([self.heading])
    self.__speed_traj = np.zeros(1, )
    self.__timeline = start_time*np.ones(1, )

  def do_step(self, beacons, SCS, ENV, dt):
    v = self.deployment_strategy.get_velocity_vector(self, beacons, SCS, ENV)
    self.__speed_traj = np.append(self.__speed_traj, np.linalg.norm(v))
    self.__timeline = np.append(self.__timeline, self.__timeline[-1] + dt)

    self.pos = euler_int(self.pos, v, dt)
    psi_ref = gva(v)
    tau = 0.1
    self.heading = euler_int(self.heading, (1/tau)*(ssa(psi_ref - self.heading)), dt)
    self._pos_traj = np.hstack((self._pos_traj, self.pos.reshape(2, 1)))
    self._heading_traj = np.concatenate((self._heading_traj, [self.heading]))
    self.state_traj = np.concatenate((self.state_traj, [self.state]))
  
  def get_timeline(self):
        return self.__timeline
  
  def get_speed_traj(self):
        return self.__speed_traj
  

  """""
  PLOTTING STUFF
  """""
  def plot(self, axis):
    self.heading_arrow = plot_vec(axis, p2v(1, self.heading), self.pos)
    return super().plot(axis, clr=self.clr[self.state]) + (self.heading_arrow, )

  def plot_traj_line(self, axis):
    self.traj_line, = axis.plot(*self._pos_traj, alpha=0.4)
    return self.traj_line

  def plot_pos_from_pos_traj_index(self, index):
    new_pos = self._pos_traj[:, index]
    self.point.set_data(new_pos)
    self.point.set_color(self.clr[self.state_traj[index]])
    self.annotation.set_x(new_pos[0])
    self.annotation.set_y(new_pos[1])
    self.traj_line.set_data(self._pos_traj[:, :index])

    self.heading_arrow.set_data(*np.hstack((new_pos.reshape(2, 1), new_pos.reshape(2, 1) + p2v(1, self._heading_traj[index]).reshape(2, 1))))
    return self.point, self.annotation, self.traj_line, self.heading_arrow