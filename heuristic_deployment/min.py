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

  def __init__(self, max_range):
    super().__init__(max_range, None)
    self.sensors = []
    for ang in np.arange(0, 360, 90):
      r = RangeSensor(max_range)
      r.mount(self, ang)

  def insert_into_environment(self, env):
    super().insert_into_environment(env)
    self._pos_traj = self.pos.reshape(2, 1)
    self._heading_traj = np.zeros((1, ))
    self.speed = 0
    self.state = MinState.SPAWNED

  def get_exploration_dir(self, k, rand_lim = 0.1):
    angs_to_neighs = gva(np.array([
        self.get_vec_to_other(n) for n in self.neighbors
    ]).T)
    num_neighs_of_neighs = np.array([
      len(n.neighbors) for n in self.neighbors
    ])

    alphas = num_neighs_of_neighs < k
    sum_alphas = np.sum(alphas)
    theta1 = np.sum(alphas*angs_to_neighs)/sum_alphas if sum_alphas > 0 else 0
    theta2 = np.random.uniform(-rand_lim, rand_lim)
    return theta1 + 0*theta2

  def get_obstacle_avoidance_vec(self, env):
    xtra_heading_vec = np.zeros((2, ))
    for s in self.sensors:
      r = s.sense(env).get_val()
      if not r == np.inf:
        abs_ang = self.heading + s.host_relative_angle
        xtra_heading_vec += -p2v(1 - r/s.max_range, abs_ang)
    return xtra_heading_vec

  def set_heading_and_speed(self, heading, speed = None):
    assert speed >= 0, "Trying to set MIN speed to something negative is not allowed."
    self.heading = heading
    if not speed is None:
      self.speed = speed

  def do_step(self, sampling_time):
    self.pos = self.pos + p2v(1, self.heading)*self.speed*sampling_time
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