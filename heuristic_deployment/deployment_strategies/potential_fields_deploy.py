import numpy as np

from deployment_strategies.deployment_strategy import (
    DeploymentStrategy,
    FollowingStrategy,
    FollowingStrategyType
)
from deployment_strategies.deployment_helpers import (
    get_neighbor_forces as gnf,
    get_obstacle_forces as gof
)
from min import MinState
from helpers import (
    polar_to_vec as p2v,
    get_vector_angle as gva,
    rot_z_mat as R_z,
    normalize
)

class PotentialFieldsDeploy(DeploymentStrategy):

    def __init__(self, K_n=1, K_o=1, min_force_threshold=0.1, following_strategy=FollowingStrategy(FollowingStrategyType.SAFE), if_same_num_neighs="nearest"):
        super().__init__(following_strategy, if_same_num_neighs)
        self.__K_n = K_n
        self.__K_o = K_o
        self.__min_force_threshold = min_force_threshold
    
    def get_exploration_velocity(self, MIN, beacons, ENV):
        MIN.compute_neighbors(beacons)
        F_n = gnf(self.__K_n, MIN)
        F_o = gof(self.__K_o, MIN, ENV)
        F_sum = F_n + F_o
        v = np.zeros((2, ))
        if np.linalg.norm(F_sum) > self.__min_force_threshold and MIN.get_RSSI(self.target) >= np.exp(-self.MIN_RSSI_STRENGTH_BEFORE_LAND):
            v = F_sum if np.linalg.norm(F_sum) < self.MAX_EXPLORATION_SPEED else  self.MAX_EXPLORATION_SPEED*normalize(F_sum)
        else:
            MIN.state = MinState.LANDED
        return v