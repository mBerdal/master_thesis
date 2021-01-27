from beacon import Beacon
from path_tree import PathTree

class SCS(Beacon):

    def __init__(self, range, pos=None):
        super().__init__(range, pos)
        self.path_tree = PathTree(self)