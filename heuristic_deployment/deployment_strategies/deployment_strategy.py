from min import MinState
from helpers import get_vector_angle as gva

from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class FollowingStrategy(Enum):
    DIRECT = 1,
    SAFE   = 2

class DeploymentStrategy(ABC):

    MIN_RSSI_STRENGTH_BEFORE_LAND = 2.9
    MIN_RSSI_STRENGTH_BEFORE_EXPLORE = 1

    def __init__(self, following_strategy=FollowingStrategy.SAFE):
        self.following_strategy = following_strategy
        self.target = None
        self.heading = 0
        self.speed = 0


    def follow(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED:
            self.target = self.__compute_target(beacons, SCS)
            print(f"{MIN.ID} targeting {self.target.ID}")
            if self.following_strategy == FollowingStrategy.SAFE:
                self.__beacons_to_follow = SCS.path_tree.get_beacon_path_to_target(self.target.ID)
                SCS.path_tree.add_node(MIN, self.target.ID)
            else:
                self.__beacons_to_follow = [self.target]
            MIN.state = MinState.FOLLOWING
            self.__btf = self.__beacons_to_follow.pop(0)
            self.heading = gva(MIN.get_vec_to_other(self.__btf))
            self.speed = 2
        if MIN.get_RSSI(self.__btf) >= np.exp(-self.MIN_RSSI_STRENGTH_BEFORE_EXPLORE):
            try:
                self.__btf = self.__beacons_to_follow.pop(0)
                self.heading = gva(MIN.get_vec_to_other(self.__btf))
            except IndexError:
                MIN.state = MinState.EXPLORING
                MIN.compute_neighbors(beacons)
                self.speed = 0
        return self.heading, self.speed
    

    @staticmethod
    def __compute_target(beacons, SCS):
        target = beacons[0]
        if len(beacons) > 1:
            tmp = beacons[1:]
            num_neighs = np.array([len(b.neighbors) for b in tmp])
            min_neigh_indices, = np.where(num_neighs == num_neighs.min())
            if len(min_neigh_indices) > 1:
                return min(tmp[min_neigh_indices], key=lambda beacon: np.linalg.norm(SCS.get_vec_to_other(beacon)))
            else:
                return tmp[min_neigh_indices[0]]
        return target

    @abstractmethod
    def explore(self, MIN, beacons, ENV):
        pass

    @abstractmethod
    def get_heading_and_speed(self, MIN, beacons, SCS, ENV):
        pass