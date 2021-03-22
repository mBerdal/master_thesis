import numpy as np
from helpers import plot_vec

class Beacon():

  ID_counter = 0

  @staticmethod
  def get_ID():
    ret = Beacon.ID_counter
    Beacon.ID_counter += 1
    return ret

  def __init__(self, xi_max, d_perf, d_none, k=0, a=0, exploration_dir=np.zeros((2, )), pos=None):
    self.pos = pos
    self.ID = self.get_ID()
    self.neighbors = []
    """ STUFF FOR XI MODEL """
    self.xi_max = xi_max
    self.d_perf = d_perf
    self.d_none = d_none
    self._omega = np.pi/(self.d_none - self.d_perf)
    self._phi = -np.pi*self.d_perf/(self.d_none - self.d_perf)
    self._xi_max_decrease = (xi_max/2)*self._omega
    """ Gains """
    self.k = k
    self.a = a
    """ xi direction vector for 2D exploration """
    self.exploration_dir = exploration_dir
  
  def insert_into_environment(self, env):
    self.pos = env.entrance_point
  
  def get_xi_to_other_from_model(self, other):
    d = np.linalg.norm(self.pos - other.pos)
    if d < self.d_perf:
      return self.xi_max
    if d > self.d_none:
      return 0
    return (self.xi_max/2)*(1+np.cos(self._omega*d + self._phi))

  def get_xi_max_decrease(self):
    return self._xi_max_decrease


  def get_vec_to_other(self, other):
    return other.pos - self.pos
  
  def __eq__(self, other):
        return self.ID == other.ID
  
  def __str__(self):
        return f"[\n\ttype: {self.__class__.__name__},\n\tID:{self.ID},\n\tneighbors: {len(self.neighbors)},\n\tpos: {self.pos}\n]"


  """""
  PLOTTING STUFF
  """""
  def plot(self, axis, clr="green"):
    self.point = axis.plot(*self.pos, color=clr, marker="o", markersize=8)[0]
    self.annotation = axis.annotate(self.ID, xy=(self.pos[0], self.pos[1]), fontsize=14)
    self.exploration_arrow = plot_vec(axis, self.exploration_dir, self.pos, clr="green")
    return self.point, self.annotation, self.exploration_arrow