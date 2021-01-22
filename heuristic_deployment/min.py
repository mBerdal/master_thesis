from beacon import Beacon
from range_sensor import RangeSensor
import numpy as np
from helpers import polar_to_vec as p2v, normalize

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
    self.heading_traj = np.zeros((2, 1))
    self.nominal_heading_traj = np.zeros((2, 1))
    self.obs_avoidance_heading_traj = np.zeros((2, 1))
    self.speed = 0
    self.state = MinState.SPAWNED

  @staticmethod
  def get_exploration_dir(bearing_to_neighbors, num_neighbors_of_neighbors, k=3, rand_lim = 0.1):
    alphas = num_neighbors_of_neighbors < k
    sum_alphas = np.sum(alphas)
    theta1 = np.sum(alphas*bearing_to_neighbors)/sum_alphas if sum_alphas > 0 else 0
    theta2 = np.random.uniform(-rand_lim, rand_lim)
    return theta1 + theta2

  def get_obstacle_avoidance_heading(self, env):
    xtra_heading_vec = np.zeros((2, ))
    for s in self.sensors:
      r = s.sense(env).get_val()
      if not r == np.inf:
        abs_ang = np.arctan2(self.heading[1], self.heading[0]) + s.host_relative_angle
        xtra_heading_vec += -p2v(1/r - 1/s.max_range, abs_ang)
    return xtra_heading_vec

  def set_heading_and_speed(self, nominal_heading, obs_avoidance_heading = np.zeros((2, )), speed = None):
    assert speed is None or speed >= 0
    self.nominal_heading = normalize(nominal_heading)
    self.obs_avoidance_heading = obs_avoidance_heading
    self.heading = normalize(nominal_heading + obs_avoidance_heading)
    if not speed is None:
      self.speed = speed

  def do_step(self, sampling_time):
    self.pos = self.pos + self.heading*self.speed*sampling_time
    self.pos_traj = np.hstack((self.pos_traj, self.pos.reshape(2, 1)))
    self.heading_traj = np.hstack((self.heading_traj, self.heading.reshape(2, 1)))
    self.nominal_heading_traj = np.hstack((self.nominal_heading_traj, self.nominal_heading.reshape(2, 1)))
    self.obs_avoidance_heading_traj = np.hstack((self.obs_avoidance_heading_traj, self.obs_avoidance_heading.reshape(2, 1)))
  
  def plot(self, axis):
    self.arrow_heading, = axis.plot(*np.vstack((self.pos, self.pos + self.heading)).T, color="blue")
    self.arrow_nominal_heading, = axis.plot(*np.vstack((self.pos, self.pos + self.nominal_heading)).T, color="green")
    self.arrow_obs_avoidance_heading, = axis.plot(*np.vstack((self.pos, self.pos - self.obs_avoidance_heading)).T, color="red")
    return super().plot(axis, clr="blue") + (self.arrow_heading, self.arrow_nominal_heading, self.arrow_obs_avoidance_heading)

  def plot_traj_line(self, axis):
    self.traj_line, = axis.plot(*self.pos_traj, alpha=0.4)
    return self.traj_line

  def plot_pos_from_pos_traj_index(self, index):
    new_pos = self.pos_traj[:, index]
    self.point.set_data(new_pos)
    self.annotation.set_x(new_pos[0])
    self.annotation.set_y(new_pos[1])
    theta = np.linspace(0, 2*np.pi)
    self.radius.set_data(new_pos.reshape(2, 1) + p2v(self.range, theta))
    self.traj_line.set_data(self.pos_traj[:, :index])

    self.arrow_heading.set_data(*np.vstack((new_pos, new_pos + self.heading_traj[:, index])).T)
    self.arrow_nominal_heading.set_data(*np.vstack((new_pos, new_pos + self.nominal_heading_traj[:, index])).T)
    self.arrow_obs_avoidance_heading.set_data(*np.vstack((new_pos, new_pos - self.obs_avoidance_heading_traj[:, index])).T)

    return self.point, self.annotation, self.radius, self.traj_line, self.arrow_heading, self.arrow_nominal_heading, self.arrow_obs_avoidance_heading
  
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
  mn.pos = 9*np.ones((2, ))
  mn.set_heading_and_speed(p2v(1, 0), np.zeros((2, )), 0)
  obs_vec = mn.get_obstacle_avoidance_heading(env)
  mn.set_heading_and_speed(p2v(1, 0), obs_vec, 1)
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots()
  env.plot(ax)
  mn.plot(ax)
  plt.show()
