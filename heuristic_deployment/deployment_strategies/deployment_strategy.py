from min import MinState
from helpers import normalize

from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class FollowingStrategy(Enum):
    DIRECT = 1,
    SAFE   = 2

class DeploymentStrategy(ABC):

    FOLLOWING_SPEED = 2

    def __init__(self, following_strategy=FollowingStrategy.SAFE):
        self.following_strategy = following_strategy
        self.target = None
        self.v = None

    def get_velocity_vector(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED or MIN.state == MinState.FOLLOWING:
            return self.follow(MIN, beacons, SCS, ENV)
        elif MIN.state == MinState.EXPLORING:
            return self.explore(MIN, beacons, ENV)
        else:
            print("MIN ALREADY LANDED")
            exit(0)

    def follow(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED:
            self.v = np.zeros((2, ))
            self.target = self.__compute_target(beacons, SCS)
            if self.following_strategy == FollowingStrategy.SAFE:
                self.__beacons_to_follow = SCS.path_tree.get_beacon_path_to_target(self.target.ID)
                SCS.path_tree.add_node(MIN, self.target.ID)
            else:
                self.__beacons_to_follow = [self.target]
            MIN.state = MinState.FOLLOWING
            self.__btf = self.__beacons_to_follow.pop(0)
        if MIN.get_RSSI(self.__btf) >= np.exp(-0.2):
            try:
                self.__btf = self.__beacons_to_follow.pop(0)
                self.v = self.FOLLOWING_SPEED*normalize(MIN.get_vec_to_other(self.__btf))
            except IndexError:
                MIN.state = MinState.EXPLORING
                MIN.compute_neighbors(beacons)
                return self.explore(MIN, beacons, ENV)
        return self.v
    
    def __compute_target(self, beacons, SCS):
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
