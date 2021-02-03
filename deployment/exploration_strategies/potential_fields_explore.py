from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)
from deployment.deployment_helpers import (
    get_neighbor_forces as gnf,
    get_obstacle_forces as gof
)
from helpers import normalize

import numpy as np

class PotentialFieldsExplore(ExplorationStrategy):
    
    def __init__(self, K_n=1, K_o=1, min_force_threshold=0.1):
        self.__K_n = K_n
        self.__K_o = K_o
        self.__min_force_threshold = min_force_threshold

    def get_exploration_velocity(self, MIN, beacons, ENV):
        MIN.compute_neighbors(beacons)
        F_n = gnf(self.__K_n, MIN)
        F_o = gof(self.__K_o, MIN, ENV)
        F_sum = F_n + F_o
        if np.linalg.norm(F_sum) > self.__min_force_threshold and MIN.get_RSSI(self.target) >= self.MIN_RSSI_STRENGTH_BEFORE_LAND:
            return F_sum if np.linalg.norm(F_sum) < self.MAX_EXPLORATION_SPEED else self.MAX_EXPLORATION_SPEED*normalize(F_sum)
        raise AtLandingConditionException