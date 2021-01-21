from beacon import Beacon
from range_sensor import RangeSensor
import numpy as np

from enum import Enum

class MinState(Enum):
  SPAWNED   = 0,
  FOLLOWING = 1,
  EXPLORING = 2,
  LANDED    = 3

class Min(Beacon):

  def __init__(self, max_range):
    super().__init__(max_range, None)
    self.sensors = []
    for ang in np.arange(0, 360, 90):
      r = RangeSensor(max_range)
      r.mount(self, ang)

  def insert_into_environment(self, env):
    super().insert_into_environment(env)
    self.pos_traj = self.pos.reshape(2, 1)
    self.heading_traj = np.zeros((1, ))
    self.speed = 0
    self.state = MinState.SPAWNED

  @staticmethod
  def get_exploration_dir(bearing_to_neighbors, num_neighbors_of_neighbors, k=3, rand_lim = 0.1):
    alphas = num_neighbors_of_neighbors < k
    sum_alphas = np.sum(alphas)
    theta1 = np.sum(alphas*bearing_to_neighbors)/sum_alphas if sum_alphas > 0 else 0
    theta2 = np.random.uniform(-rand_lim, rand_lim)
    return theta1 + theta2

  def set_heading_and_speed(self, heading, speed = None):
    assert speed is None or speed >= 0
    self.heading = heading
    if not speed is None:
      self.speed = speed

  def do_step(self, sampling_time):
    self.pos = self.pos + np.array([np.cos(self.heading), np.sin(self.heading)])*self.speed*sampling_time
    self.pos_traj = np.hstack((self.pos_traj, self.pos.reshape(2, 1)))
    self.heading_traj = np.hstack((self.heading_traj, self.heading))
  
  def plot(self, axis):
    self.arrow = axis.plot(
      [self.pos[0], self.pos[0] + np.cos(self.heading)],
      [self.pos[1], self.pos[1] + np.sin(self.heading)],
      color="blue"
    )[0]
    return super().plot(axis, clr="blue") + (self.arrow, )

  def plot_traj_line(self, axis):
    self.traj_line = axis.plot(*self.pos_traj, alpha=0.4)[0]
    return self.traj_line

  def plot_pos_from_pos_traj_index(self, index):
    new_pos = self.pos_traj[:, index]
    self.point.set_xdata(new_pos[0])
    self.point.set_ydata(new_pos[1])
    self.annotation.set_x(new_pos[0])
    self.annotation.set_y(new_pos[1])
    theta = np.linspace(0, 2*np.pi)
    self.radius.set_xdata(new_pos[0] + self.range*np.cos(theta))
    self.radius.set_ydata(new_pos[1] + self.range*np.sin(theta))
    self.traj_line.set_xdata(self.pos_traj[0, :index])
    self.traj_line.set_ydata(self.pos_traj[1, :index])

    self.arrow.set_xdata([new_pos[0], new_pos[0] + np.cos(self.heading_traj[index])])
    self.arrow.set_ydata([new_pos[1], new_pos[1] + np.sin(self.heading_traj[index])])

    return self.point, self.annotation, self.radius, self.traj_line, self.arrow
  
  def __str__(self):
    return f"min drone {self.ID} at {self.pos}"


if __name__ == "__main__":
  from environment import Env
  env = Env(np.array([
    [-10, -10],
    [ 10, -10],
    [ 10,  10],
    [-10,  10]
  ]), np.array([
    -9.8, -9.8
  ]))
  
  mn = Min(3)
  mn.pos = np.array([9.99, -9.1])

  from helpers import polar_to_vec as p2v

  nominal_heading = 0
  nominal_heading_vec = p2v(1, nominal_heading)
  mn.set_heading_and_speed(nominal_heading, 0)

  xtra_heading_vec = np.zeros((2, ))
  for s in mn.sensors:
    r = s.sense(env).get_val()
    abs_ang = nominal_heading + s.host_relative_angle
    xtra_heading_vec += p2v(-1/r, abs_ang)
  total_heading_vec = nominal_heading_vec + xtra_heading_vec
  total_heading = np.arctan2(total_heading_vec[1], np.rad2deg(total_heading_vec[0]))
  print(np.rad2deg(total_heading))