from matplotlib.patches import Polygon

class Segment():
      
      def __init__(self, start, end):
            self.start = start
            self.end = end
            self.vec = self.end - self.start


class Env():

    """Class representing an environment.

    Args:
        entrance_point (ndarray): 2-by-0 numpy array containing (x, y)-coords of 
        environment entrance point.

        obstacle_corners (list, optional): List of n-by-2 numpy arrays. Each numpy array contains 
        the corners of a polygon. It is assumed that there is a line between the 
        first corner and the last corner. Defaults to [].
    """

    def __init__(self, entrance_point, obstacle_corners=[]):
        self.obstacle_corners = obstacle_corners
        self.entrance_point = entrance_point
        self.__init_obstacles_as_list_of_segments()

    def __init_obstacles_as_list_of_segments(self):
        self.list_of_segments = []
        for i in range(len(self.obstacle_corners)):
            for j in range(self.obstacle_corners[i].shape[0]):
                  self.list_of_segments.append(
                    Segment(
                      self.obstacle_corners[i][j, :],
                      self.obstacle_corners[i][j-1, :]
                    )
                  )
        
    def plot(self, axis):
        for i in range(len(self.obstacle_corners)):
            axis.add_patch(Polygon(self.obstacle_corners[i], fill=False))
