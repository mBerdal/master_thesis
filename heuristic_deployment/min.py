from beacon import Beacon
from range_sensor import RangeSensor
import numpy as np
from helpers import polar_to_vec as p2v, normalize, get_vector_angle as gva, plot_vec

from enum import Enum

class MinState(Enum):
  SPAWNED   = 0,
  FOLLOWING = 1,
  EXPLORING = 2,
  LANDED    = 3

class Min(Beacon):

  def __init__(self, max_range, deployment_strategy):
    super().__init__(max_range, None)
    self.deployment_strategy = deployment_strategy
    self.sensors = []
    for ang in np.arange(0, 360, 90):
      r = RangeSensor(max_range)
      r.mount(self, ang)

  def insert_into_environment(self, env):
    super().insert_into_environment(env)
    self._pos_traj = self.pos.reshape(2, 1)
    self._heading_traj = np.zeros((1, ))
    self.speed = 0
    self.heading = 0
    self.state = MinState.SPAWNED

  def set_heading_and_speed(self, heading, speed = None):
    assert speed >= 0, "Trying to set MIN speed to something negative is not allowed."
    self.heading = heading
    if not speed is None:
      self.speed = speed

  def do_step(self, beacons, SCS, ENV, dt):
    psi, V = self.deployment_strategy.get_heading_and_speed(self, beacons, SCS, ENV)
    self.set_heading_and_speed(psi, V)
    self.pos = self.pos + p2v(1, self.heading)*self.speed*dt
    self._pos_traj = np.hstack((self._pos_traj, self.pos.reshape(2, 1)))
    self._heading_traj = np.concatenate((self._heading_traj, [self.heading]))
  
  def get_pos_traj_length(self):
        return self._pos_traj.shape[1]

  """""
  PLOTTING STUFF
  """""
  def plot(self, axis):
    self.heading_arrow = plot_vec(axis, p2v(1, self.heading), self.pos)
    return super().plot(axis, clr="blue") + (self.heading_arrow, )

  def plot_traj_line(self, axis):
    self.traj_line, = axis.plot(*self._pos_traj, alpha=0.4)
    return self.traj_line

  def plot_pos_from_pos_traj_index(self, index):
    new_pos = self._pos_traj[:, index]
    self.point.set_data(new_pos)
    self.annotation.set_x(new_pos[0])
    self.annotation.set_y(new_pos[1])
    theta = np.linspace(0, 2*np.pi)
    self.radius.set_data(new_pos.reshape(2, 1) + p2v(self.range, theta))
    self.traj_line.set_data(self._pos_traj[:, :index])

    self.heading_arrow.set_data(*np.hstack((new_pos.reshape(2, 1), new_pos.reshape(2, 1) + p2v(1, self._heading_traj[index]).reshape(2, 1))))
    return self.point, self.annotation, self.radius, self.traj_line, self.heading_arrow