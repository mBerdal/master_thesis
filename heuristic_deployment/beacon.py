import numpy as np

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
  
  def insert_into_environment(self, env):
    self.pos = env.entrance_point
  
  def is_within_range(self, other):
    dist = np.linalg.norm(self.pos - other.pos)
    return dist < self.range and dist < other.range

  def is_within_circle_of_acceptance(self, other):
    return np.linalg.norm(self.pos - other.pos) <= 0.01
  
  def get_RSSI(self, other):
    return np.exp(-np.linalg.norm(self.pos - other.pos))

  def get_num_neighbors(self, others):
    return np.count_nonzero(
      [self.is_within_range(other) and self.ID != other.ID for other in others]
    )
  
  def get_neighbors(self, others):
    return list(filter(lambda other: self.is_within_range(other) and other.ID != self.ID, others))

  def get_bearing_to_other(self, other):
    return np.arctan2(other.pos[1] - self.pos[1], other.pos[0] - self.pos[0])
  
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


