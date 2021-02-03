from matplotlib.patches import Polygon

class Env():

  def __init__(self, entrance_point, obstacle_corners = []):
    self.obstacle_corners = obstacle_corners
    self.entrance_point = entrance_point

  def plot(self, axis):
    for i in range(len(self.obstacle_corners)):
      axis.add_patch(Polygon(self.obstacle_corners[i], fill=False))