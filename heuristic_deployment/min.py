from beacon import Beacon
import numpy as np

from enum import Enum

class MinState(Enum):
  SPAWNED   = 0,
  FOLLOWING = 1,
  EXPLORING = 2,
  LANDED    = 3

class Min(Beacon):

  def __init__(self, range):
    super().__init__(range, None)

  def insert_into_environment(self, env):
    super().insert_into_environment(env)
    self.speed = 0
    self.state = MinState.SPAWNED

  @staticmethod
  def get_exploration_dir(bearing_to_neighbors, num_neighbors_of_neighbors, k=2, rand_lim = 1):
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
  
  def plot(self, axis):
    return super().plot(axis, clr="blue")

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

    return self.point, self.annotation, self.radius, self.traj_line
    self.traj_log = np.hstack((self.traj_log, self.pos.reshape(2, 1)))
  
  def __str__(self):
    return f"min drone at {self.pos}"