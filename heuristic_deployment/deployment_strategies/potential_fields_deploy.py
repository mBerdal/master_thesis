import numpy as np

from deployment_strategies.deployment_strategy import DeploymentStrategy, FollowingStrategy
from min import MinState
from helpers import polar_to_vec as p2v, get_vector_angle as gva, normalize

class PotentialFieldsDeploy(DeploymentStrategy):

    MAX_EXPLORATION_SPEED = 2

    def __init__(self, K_n=1, K_o=1, min_force_threshold=0.1, following_strategy=FollowingStrategy.SAFE):
        super().__init__(following_strategy)
        self.__K_n = K_n
        self.__K_o = K_o
        self.__min_force_threshold = min_force_threshold
        self.__x_dot = np.zeros((2, ))
    
    def explore(self, MIN, beacons, ENV):
        MIN.compute_neighbors(beacons)
        F_n = self.__get_neighbor_forces(MIN)
        F_o = self.__get_obstacle_forces(MIN, ENV)
        F_sum = F_n + F_o

        if np.linalg.norm(F_sum) > self.__min_force_threshold and MIN.get_RSSI(self.target) >= np.exp(-self.MIN_RSSI_STRENGTH_BEFORE_LAND):
            self.v = F_sum if np.linalg.norm(F_sum) < self.MAX_EXPLORATION_SPEED else  self.MAX_EXPLORATION_SPEED*normalize(F_sum)
        else:
            MIN.state = MinState.LANDED
        return self.v
        

    def __get_neighbor_forces(self, MIN):
        vecs_to_neighs = [
            MIN.get_vec_to_other(n).reshape(2, 1) for n in MIN.neighbors if not (MIN.get_vec_to_other(n) == 0).all()
        ]
        return self.__get_generic_force_vector(vecs_to_neighs, self.__K_n)

    def __get_obstacle_forces(self, MIN, ENV):
        vecs_to_obs = [
            p2v(s.sense(ENV).get_val(), MIN.heading + s.host_relative_angle).reshape(2, 1) for s in MIN.sensors if not s.sense(ENV).get_val() == np.inf
        ]
        return self.__get_generic_force_vector(vecs_to_obs, self.__K_o)

    @staticmethod
    def __get_generic_force_vector(vecs, gain):
        try:
            mat = np.concatenate(vecs, axis=1)
            return -gain*np.sum(mat/np.linalg.norm(mat, axis=0)**3, axis=1)
        except ValueError:
            return np.zeros((2, ))