from min import MinState
import numpy as np
from enum import Enum
from helpers import get_vector_angle as gva, polar_to_vec as p2v

from deployment_strategies.deployment_strategy import DeploymentStrategy

class FollowingStrategy(Enum):
    DIRECT = 1,
    SAFE   = 2

class HeuristicDeploy(DeploymentStrategy):
    
    def __init__(self, k=3):
        self.k = k
        self.__target = None
        self.__heading = 0
        self.__speed = 0

    def get_heading_and_speed(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED or MIN.state == MinState.FOLLOWING:
            return self.follow(MIN, beacons, SCS, ENV)
        elif MIN.state == MinState.EXPLORING:
            return self.explore(MIN, beacons, ENV)
        else:
            print("MIN ALREADY LANDED")
            exit(0)
    
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

    def follow(self, MIN, beacons, SCS, ENV, following_strategy=FollowingStrategy.SAFE):
        if MIN.state == MinState.SPAWNED:
            self.__target = self.__compute_target(beacons, SCS)
            if following_strategy == FollowingStrategy.SAFE:
                self.__beacons_to_follow = SCS.path_tree.get_beacon_path_to_target(self.__target.ID)
                SCS.path_tree.add_node(MIN, self.__target.ID)
            else:
                self.__beacons_to_follow = [self.__target]
            MIN.state = MinState.FOLLOWING
            self.__btf = self.__beacons_to_follow.pop(0)
        if MIN.get_RSSI(self.__btf) >= np.exp(-0.3):
            try:
                self.__btf = self.__beacons_to_follow.pop(0)
                self.__heading = gva(MIN.get_vec_to_other(self.__btf))
                self.__speed = 2
            except IndexError:
                return self.explore(MIN, beacons, ENV)
        return self.__heading, self.__speed


    def explore(self, MIN, beacons, ENV):
        if MIN.state == MinState.FOLLOWING:
            MIN.state = MinState.EXPLORING
            MIN.compute_neighbors(beacons)
            self.__exploration_dir = HeuristicDeploy.__get_exploration_dir(MIN, self.k)
            self.__exploration_vec = p2v(1, self.__exploration_dir)
            self.__speed = 1
        
        obs_vec = HeuristicDeploy.__get_obstacle_avoidance_vec(MIN, ENV)
        self.__heading = gva(self.__exploration_vec + obs_vec)
        if np.abs(self.__exploration_dir - gva(self.__exploration_vec + obs_vec)) > np.pi/2 or MIN.get_RSSI(self.__target) < np.exp(-2.6):
            MIN.state = MinState.LANDED
            self.__speed = 0
        return self.__heading, self.__speed

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
            r = s.sense(ENV).get_val()
            if not r == np.inf:
                abs_ang = MIN.heading + s.host_relative_angle
                xtra_heading_vec += -p2v(1 - r/s.max_range, abs_ang)
        return xtra_heading_vec
