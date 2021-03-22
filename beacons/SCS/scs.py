from beacons.beacon import Beacon
from beacons.SCS.path_tree import PathTree
import numpy as np

class SCS(Beacon):

    def __init__(self, xi_max, d_perf, d_none, k=1, a=1, exploration_dir=np.array([1, 0]), pos=None):
        super().__init__(xi_max, d_perf, d_none, k, a, exploration_dir, pos)
        self.path_tree = PathTree(self)