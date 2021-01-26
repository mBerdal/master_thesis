import numpy as np
from helpers import normalize

class Beacon():

  ID_counter = 0

  @classmethod
  def get_ID(cls):
    ret = cls.ID_counter
    cls.ID_counter += 1
    return ret

  def __init__(self, range, pos=None):
    self.range = range
    self.pos = pos
    self.ID = self.get_ID()
    self.neighbors = []
  
  def insert_into_environment(self, env):
    self.pos = env.entrance_point
  
  def is_within_range(self, other):
    dist = np.linalg.norm(self.pos - other.pos)
    return dist < self.range and dist < other.range

  def is_within_circle_of_acceptance(self, other):
    return np.linalg.norm(self.pos - other.pos) <= 0.01

  def compute_neighbors(self, others):
    self.neighbors = list(filter(lambda other: self.is_within_range(other) and self != other, others))
  
  def get_RSSI(self, other):
    return np.exp(-np.linalg.norm(self.pos - other.pos))

  def get_vec_to_other(self, other):
    return other.pos - self.pos
  
  def __eq__(self, other):
        return self.ID == other.ID


  """""
  PLOTTING STUFF
  """""
  def plot(self, axis, clr="green"):
    self.point = axis.plot(*self.pos, color=clr, marker="o", markersize=8)[0]
    self.annotation = axis.annotate(self.ID, xy=(self.pos[0], self.pos[1]), fontsize=14)
    theta = np.linspace(0, 2*np.pi)
    self.radius = axis.plot(
      self.pos[0] + self.range*np.cos(theta), self.pos[1] + self.range*np.sin(theta),
      linestyle="dashed",
      color="black",
      alpha=0.3
    )[0]

    return self.point, self.annotation, self.radius


