from beacons.beacon import Beacon
from beacons.SCS.path_tree import PathTree

class SCS(Beacon):

    def __init__(self, range, pos=None):
        super().__init__(range, pos)
        self.path_tree = PathTree(self)