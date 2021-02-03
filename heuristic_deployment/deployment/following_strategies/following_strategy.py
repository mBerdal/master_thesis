from helpers import normalize
from min import MinState 
from deployment.deployment_helpers import (
    get_obstacle_forces as gof
)

from abc import ABC, abstractmethod
import numpy as np

class AtTargetException(Exception):
    """
    Raised when there are no more beacons, i.e. the 
    MIN has arrived sufficiently close to its target.
    """

class FollowingStrategy(ABC):

    MAX_FOLLOWING_SPEED = 2
    MIN_RSSI_STRENGTH_BEFORE_EXPLORE = np.exp(-0.1)

    def __init__(self, same_num_neighs_differentiator):
        self.__snnd = same_num_neighs_differentiator
        self.beacons_to_follow = None

    def compute_next_beacon_to_follow(self):
        self.btf = self.beacons_to_follow.pop(0)

    def is_following_target(self):
        return self.btf == self.target

    @abstractmethod
    def prepare_following(self, MIN, beacons, SCS):
        self.__compute_target(beacons, SCS)

    @abstractmethod
    def get_following_velocity(self, MIN, ENV):
        pass
    
    def __compute_target(self, beacons, SCS):
        self.target = beacons[0]
        if len(beacons) > 1:
            tmp = beacons[1:]
            num_neighs = np.array([len(b.neighbors) for b in tmp])
            min_neigh_indices, = np.where(num_neighs == num_neighs.min())
            if len(min_neigh_indices) > 1:
                self.target =  self.__snnd(tmp[min_neigh_indices], lambda beacon: np.linalg.norm(SCS.get_vec_to_other(beacon)))
            else:
                self.target = tmp[min_neigh_indices[0]]

    @staticmethod
    def follow_velocity_wrapper(func):
        def func_wrapper(*args):
            fs, MIN, _ = args
            if MIN.get_RSSI(fs.btf) >= FollowingStrategy.MIN_RSSI_STRENGTH_BEFORE_EXPLORE:
                if fs.is_following_target():
                    raise AtTargetException
                fs.compute_next_beacon_to_follow()
            return func(*args)
        return func_wrapper