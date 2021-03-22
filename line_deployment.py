from deployment_helpers import get_obstacle_forces as gof, AtLandingConditionException
from helpers import normalize, rot_mat_2D, get_vector_angle as gva

import numpy as np


class LineDeployment():

    TAU_XI = 0.5

    def __init__(self, field_type=1, K_o=1, force_threshold=0.01,
                get_exploration_dir_callback= lambda MIN, neighs, F_O: None):
        assert field_type in [1, 2], "field_type must either be 1 or 2"
        self.__get_neigh_force = [
            self.__get_force_type_1,
            self.__get_force_type_2
        ][field_type-1]

        self.K_o = K_o
        self.force_threshold = force_threshold
        self.get_exploration_dir_callback = get_exploration_dir_callback

    def init_deployment(self, MIN, deployed_beacons, ENV):
        self.MIN = MIN
        self.ENV = ENV
        self.deployed_beacons = deployed_beacons

        self.beacon_x_is = np.concatenate([b.pos.reshape(2, 1) for b in deployed_beacons], axis=1)
        self.beacon_v_is = np.concatenate([
                b.exploration_dir.reshape(2, 1) for b in deployed_beacons
            ], axis=1)

        self.prev_neigh_idx_set = set()
        self.neigh_idxs = np.empty(1, )

    def get_velocity_vector(self):
        xi_is = np.array([self.MIN.get_xi_to_other_from_model(b) for b in self.deployed_beacons])

        self.neigh_idxs, = np.where(xi_is > self.TAU_XI)
        land_due_to_no_neighs = self.neigh_idxs.shape[0] == 0
        
        if land_due_to_no_neighs:
            print(f"WARNING! {self.MIN.ID} landed due to no neighs")
        else:
            neigh_idx_set = set(self.neigh_idxs)
            if not neigh_idx_set == self.prev_neigh_idx_set:
                self.prev_neigh_idx_set = neigh_idx_set

                self.neigh_x_is = self.beacon_x_is[:, self.neigh_idxs]
                self.neigh_v_is = self.beacon_v_is[:, self.neigh_idxs]

                self.leader = np.argmax(np.array([b.ID for b in self.deployed_beacons[self.neigh_idxs]]))

                """ Testing dynamic gains """

                self.neigh_k_is = np.ones(self.neigh_idxs.shape)
                self.neigh_a_is = np.zeros(self.neigh_idxs.shape)
                self.neigh_a_is[self.leader] = self.neigh_idxs.shape[0]
        
        neigh_xi_is = xi_is[self.neigh_idxs]
        
        F_n = self.__get_neigh_force(neigh_xi_is)
        F = F_n

        at_landing_condition = land_due_to_no_neighs or np.linalg.norm(F) < self.force_threshold
        if at_landing_condition:
            neighs = self.deployed_beacons[self.neigh_idxs]
            self.MIN.exploration_dir = self.get_exploration_dir_callback(self.MIN, neighs, np.zeros(2, ))
            raise AtLandingConditionException
        return F

    def __get_force_type_1(self, neigh_xi_is):
        """Returns force created by potential field:
        U_{n+1, i} = (1/2)*norm(x_{n+1} - a_i*(x_i + xi_i*v_i))^2

        Returns:
            ndarray: total force acting on MIN from its neighbors
        """
        return -np.sum(
                self.neigh_k_is*(self.MIN.pos.reshape(2, 1) - self.neigh_a_is*(self.neigh_x_is + neigh_xi_is*self.neigh_v_is))
            ,axis=1).reshape(2, )
    
    def __get_force_type_2(self, neigh_xi_is):
        """Returns force created by potential field:
        U_{n+1, i} = (1/2)*norm(x_{n+1} - (x_i + a_i*xi_i*v_i))^2

        Returns:
            ndarray: total force acting on MIN from its neighbors
        """
        return -np.sum(
                self.neigh_k_is*(self.MIN.pos.reshape(2, 1) - (self.neigh_x_is + self.neigh_a_is*neigh_xi_is*self.neigh_v_is))
            ,axis=1).reshape(2, )

    