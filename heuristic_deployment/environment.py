from matplotlib.patches import Polygon

class Env():

  def __init__(self, corners, entrance_point):
    self.corners = corners
    self.entrance_point = entrance_point

  def plot(self, axis):
    axis.add_patch(Polygon(self.corners, fill=False))