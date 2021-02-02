from min import MinState
import numpy as np
from enum import Enum
from helpers import (
    get_vector_angle as gva,
    polar_to_vec as p2v,
    rot_z_mat as R_z,
    normalize
)
from deployment_strategies.deployment_strategy import (
    DeploymentStrategy,
    FollowingStrategy,
    FollowingStrategyType
)


class HeuristicDeploy(DeploymentStrategy):

    OBS_AVOIDANCE_GAIN = 1.1

    def __init__(self, k=3, following_strategy=FollowingStrategy(FollowingStrategyType.SAFE), if_same_num_neighs="nearest"):
        super().__init__(following_strategy, if_same_num_neighs)
        self.k = k
        self.__exploration_dir = None
        self.__exploration_vec = None

    def get_exploration_velocity(self, MIN, beacons, ENV):
        if self.__exploration_dir is None:
            self.__exploration_dir = HeuristicDeploy.__get_exploration_dir(MIN, self.k)
            self.__exploration_vec = p2v(1, self.__exploration_dir)
        
        obs_vec = HeuristicDeploy.__get_obstacle_avoidance_vec(MIN, ENV)
        v = normalize(self.__exploration_vec + obs_vec)

        if np.abs(self.__exploration_dir - gva(self.__exploration_vec + obs_vec)) > np.pi/2 or MIN.get_RSSI(self.target) < np.exp(-self.MIN_RSSI_STRENGTH_BEFORE_LAND):
            MIN.state = MinState.LANDED
        return v

    @staticmethod
    def __get_exploration_dir(MIN, k, rand_lim = 0.1):
        angs_to_neighs = gva(np.array([
            MIN.get_vec_to_other(n) for n in MIN.neighbors
        ]).T)
        num_neighs_of_neighs = np.array([
            len(n.neighbors) for n in MIN.neighbors
        ])

        alphas = num_neighs_of_neighs < k
        sum_alphas = np.sum(alphas)
        theta1 = np.sum(alphas*angs_to_neighs)/sum_alphas if sum_alphas > 0 else 0
        theta2 = np.random.uniform(-rand_lim, rand_lim)
        return theta1 + 0*theta2

    @staticmethod
    def __get_obstacle_avoidance_vec(MIN, ENV):
        xtra_heading_vec = np.zeros((2, ))
        for s in MIN.sensors:
            s.sense(ENV)
            if s.measurement.is_valid():
                v_s = np.array([HeuristicDeploy.OBS_AVOIDANCE_GAIN, 0, 0]).reshape(3, 1) - HeuristicDeploy.OBS_AVOIDANCE_GAIN*s.measurement.get_val()/s.max_range
                xtra_heading_vec += (-(R_z(MIN.heading)@R_z(s.host_relative_angle)@v_s)[:2]).reshape((2, ))
        return xtra_heading_vec