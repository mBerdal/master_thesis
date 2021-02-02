from min import MinState
from helpers import normalize
from deployment_strategies.deployment_helpers import (
    get_obstacle_forces as gof,
    get_generic_force_vector as ggnf
)
from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class FollowingStrategyType(Enum):
    DIRECT     = 1,
    SAFE       = 2,
    ATTRACTIVE = 3

class FollowingStrategy():
    def __init__(self,  following_strategy_type, **kwargs):
        assert not(following_strategy_type == FollowingStrategyType.ATTRACTIVE and not kwargs.get("K_o")),\
        "K_o must be passed as an argument when using the attractive following strategy"
        self.ftp = following_strategy_type
        self.K_o = kwargs.get("K_o")

class DeploymentStrategy(ABC):

    MAX_EXPLORATION_SPEED            = 2
    MAX_FOLLOWING_SPEED              = 2
    MIN_RSSI_STRENGTH_BEFORE_LAND    = 2.9
    MIN_RSSI_STRENGTH_BEFORE_EXPLORE = 0.1

    def __init__(self, following_strategy=FollowingStrategy(FollowingStrategyType.SAFE), if_same_num_neighs="nearest"):
        self.following_strategy = following_strategy
        self.if_same_num_neighs = if_same_num_neighs
        self.target = None
        self.v = None

    def get_velocity_vector(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED:
            print(f"MIN {MIN.ID} spawned")
            self.__init_follow(MIN, beacons, SCS)
            print(f"MIN {MIN.ID} following MIN {self.target.ID} with {len(self.target.neighbors)} neighs")
        if MIN.state == MinState.FOLLOWING:
            self.v = self.__get_following_velocity(MIN, beacons, SCS, ENV)
        elif MIN.state == MinState.EXPLORING:
            self.v = self.get_exploration_velocity(MIN, beacons, ENV)
        else:
            print("MIN ALREADY LANDED")
            exit(0)
        return self.v

    def __get_following_velocity(self, MIN, beacons, SCS, ENV):
        if MIN.get_RSSI(self.__btf) >= np.exp(-self.MIN_RSSI_STRENGTH_BEFORE_EXPLORE):
            try:
                self.__btf = self.__beacons_to_follow.pop(0)
            except IndexError:
                MIN.state = MinState.EXPLORING
                MIN.compute_neighbors(beacons)
                """
                Extra check to see if the 'new' MIN has traveled further than the previous one
                TODO: RSSI check
                TODO: Distance check
                """
                print(f"MIN {MIN.ID} exploring")
                return self.get_exploration_velocity(MIN, beacons, ENV)
        v = None
        if self.following_strategy.ftp == FollowingStrategyType.ATTRACTIVE:
            v = DeploymentStrategy.__attractive_follow(self.following_strategy.K_o, self.__btf, MIN, ENV)
        else:
            v = DeploymentStrategy.__straight_line_follow(self.__btf, MIN)
        return v

    @staticmethod
    def __attractive_follow(K_o, btf, MIN, ENV):
        F_o = gof(K_o, MIN, ENV)
        F_btf = MIN.get_vec_to_other(btf)
        F_btf_aug = DeploymentStrategy.MAX_FOLLOWING_SPEED*normalize(F_btf) if np.linalg.norm(F_btf) > DeploymentStrategy.MAX_FOLLOWING_SPEED else F_btf
        F = F_o + F_btf_aug
        """
        TODO: return a non-zero net force when the MIN the deployed MIN is following is the target
        (to ensure than we travel further into the environment)
        """
        return DeploymentStrategy.MAX_FOLLOWING_SPEED*normalize(F)
    
    @staticmethod
    def __straight_line_follow(btf, MIN):
        return DeploymentStrategy.MAX_FOLLOWING_SPEED*normalize(MIN.get_vec_to_other(btf))

    def __init_follow(self, MIN, beacons, SCS):
        self.v = np.zeros((2, ))
        self.target = self.__compute_target(beacons, SCS, self.if_same_num_neighs)
        if self.following_strategy.ftp == FollowingStrategyType.SAFE or self.following_strategy.ftp == FollowingStrategyType.ATTRACTIVE:
            self.__beacons_to_follow = SCS.path_tree.get_beacon_path_to_target(self.target.ID)
            SCS.path_tree.add_node(MIN, self.target.ID)
        else:
            self.__beacons_to_follow = [self.target]
        MIN.state = MinState.FOLLOWING
        self.__btf = self.__beacons_to_follow.pop(0)

    @staticmethod
    def __compute_target(beacons, SCS, if_same_num_neighs):
        target = beacons[0]
        if len(beacons) > 1:
            tmp = beacons[1:]
            num_neighs = np.array([len(b.neighbors) for b in tmp])
            min_neigh_indices, = np.where(num_neighs == num_neighs.min())
            if len(min_neigh_indices) > 1:
                fun = lambda MINs, k: min(MINs, key=k) if if_same_num_neighs == "nearest" else max(MINs, key=k)
                return fun(tmp[min_neigh_indices], lambda beacon: np.linalg.norm(SCS.get_vec_to_other(beacon)))
            else:
                return tmp[min_neigh_indices[0]]
        return target

    @abstractmethod
    def get_exploration_velocity(self, MIN, beacons, ENV):
        pass
