from deployment.deployment_helpers import get_obstacle_forces as gof
from helpers import normalize, rot_mat_2D, get_vector_angle as gva

import numpy as np

from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)


class TWO_DIM_LOCAL_LINE_EXPLORE(ExplorationStrategy):

    RSSI_TRHESHOLD = 0.5

    def __init__(self, K_o=1, force_threshold=0.01,
                get_exploration_dir_callback= lambda MIN, neighs, F_O: None):
        self.K_o = K_o
        self.force_threshold = force_threshold
        self.get_exploration_dir_callback = get_exploration_dir_callback

    def load_beacon_info(self, deployed_beacons):
        self.x_is = np.concatenate([b.pos.reshape(2, 1) for b in deployed_beacons], axis=1)
        self.v_is = np.concatenate([
                b.exploration_dir.reshape(2, 1) for b in deployed_beacons
            ], axis=1)
        self.prev_neigh_idxs, self.neigh_idxs = np.empty(1, ), np.empty(1, )

        self.neigh_x_is = None
        self.neigh_v_is = None

        self.neigh_k_is = None
        self.neigh_a_is = None

        self.leader = None

    def get_exploration_velocity(self, MIN, beacons, ENV):

        F_n = np.zeros((2, ))
        F_o = gof(self.K_o, MIN, ENV)

        xi_is = np.array([MIN.get_xi_to_other_from_model(b) for b in beacons])

        self.neigh_idxs, = np.where(xi_is > self.RSSI_TRHESHOLD)
        land_due_to_no_neighs = self.neigh_idxs.shape[0] == 0
        
        if land_due_to_no_neighs:
            print(f"{MIN.ID} STOPPED due to no neighs")
        else:
            
            if not set(self.neigh_idxs) == set(self.prev_neigh_idxs):
                self.prev_neigh_idxs = self.neigh_idxs

                self.neigh_x_is = self.x_is[:, self.neigh_idxs]
                self.neigh_v_is = self.v_is[:, self.neigh_idxs]
                self.leader = np.argmax(np.array([b.ID for b in beacons[self.neigh_idxs]]))

                """ Testing dynamic gains """

                self.neigh_k_is = np.ones(self.neigh_idxs.shape)
                self.neigh_a_is = np.zeros(self.neigh_idxs.shape)
                self.neigh_a_is[self.leader] = self.neigh_idxs.shape[0]

                
                """ Testing using only supporters """
                theta_l = gva(self.neigh_v_is[:, self.leader])
                x_l = self.neigh_x_is[:, self.leader]

                supporter_idxs = -1*np.ones(self.neigh_idxs.shape[0], dtype=np.int)
                for i in np.arange(self.neigh_idxs.shape[0]):
                    x_i = self.neigh_x_is[:, i]
                    theta_i = gva(self.neigh_v_is[:, i])
                    if i == self.leader or (np.abs(gva(x_i - x_l) - theta_l) <= np.pi/2 and np.abs(theta_i - theta_l) <= np.pi/2):
                        supporter_idxs[i] = i
                
                supporter_idxs = supporter_idxs[supporter_idxs > -1]
                assert self.neigh_idxs[self.leader] in self.neigh_idxs[supporter_idxs], f"{self.neigh_idxs[self.leader]} not in {self.neigh_idxs[supporter_idxs]}, neigh indices={self.neigh_idxs}"
                
                self.neigh_k_is = np.zeros(self.neigh_idxs.shape)
                self.neigh_k_is[supporter_idxs] = 1
                self.neigh_a_is = np.zeros(self.neigh_idxs.shape)
                self.neigh_a_is[supporter_idxs] = 1

            neigh_xi_is = xi_is[self.neigh_idxs]

            """ Calculating force """
            F_n = -np.sum(
                self.neigh_k_is*(MIN.pos.reshape(2, 1) - (self.neigh_x_is + self.neigh_a_is*neigh_xi_is*self.neigh_v_is)),
            axis=1).reshape(2, )
            
            F = F_n + F_o

        at_landing_condition = land_due_to_no_neighs or np.linalg.norm(F) < self.force_threshold
        if at_landing_condition:
            neighs = beacons[self.neigh_idxs]
            MIN.exploration_dir = self.get_exploration_dir_callback(MIN, neighs, F_o)
            raise AtLandingConditionException
        return F