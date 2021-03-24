from deployment_helpers import get_obstacle_forces as gof, AtLandingConditionException
from helpers import clamp
import numpy as np


class LineDeployment():

    def __init__(self, d_bar, xi_bar, tau_xi, field_type=1, K_o=1, force_threshold=0.01,
                get_exploration_dir_callback= lambda MIN, neighs, F_O: None):

        self.D_BAR = d_bar
        self.XI_BAR = xi_bar
        self.TAU_XI = tau_xi

        assert field_type in [1, 2], "field_type must either be 1 or 2"
        self.__get_neigh_force = [
            self.__get_force_type_1,
            self.__get_force_type_2
        ][field_type-1]

        self.K_o = K_o
        self.force_threshold = force_threshold
        self.get_exploration_dir_callback = get_exploration_dir_callback

        self.neighs = None


    def init_deployment(self, MIN, deployed_beacons, ENV):
        self.MIN = MIN
        self.ENV = ENV
        self.deployed_beacons = deployed_beacons

        self.beacon_x_is = np.concatenate([b.pos.reshape(2, 1) for b in deployed_beacons], axis=1)
        self.beacon_v_is = np.concatenate([
                b.exploration_dir.reshape(2, 1) for b in deployed_beacons
            ], axis=1)

        self.beacon_a_is = np.array([b.a for b in deployed_beacons])
        self.beacon_k_is = np.array([b.k for b in deployed_beacons])

        self.neigh_mask = np.ones(1, dtype=np.int8)
        self.prev_neigh_mask = np.zeros(1, dtype=np.int8)

    def get_velocity_vector(self):
        xi_is = np.array([self.MIN.get_xi_to_other_from_model(b) for b in self.deployed_beacons])
        self.neigh_mask = (xi_is > self.TAU_XI)*1

        if not ((self.neigh_mask == self.prev_neigh_mask).all() or np.flatnonzero(self.neigh_mask).size == 0):
            self.prev_neigh_mask = np.copy(self.neigh_mask)

            #self.neigh_k_is, self.neigh_a_is = self.__get_type_1_dynamic_gains()
            self.k_is, self.a_is = self.__get_static_gains()
    
        F_n = self.__get_neigh_force(xi_is)
        F = F_n

        if np.linalg.norm(F) < self.force_threshold:
            self.neighs = set(self.deployed_beacons[np.flatnonzero(self.neigh_mask)])
            if np.flatnonzero(self.neigh_mask).size == 0:
                print(f"WARNING! {self.MIN.ID} landing due to no beacons within XI threshold, using neighbor set\
                        from just before loss of neighbors")
                
                self.neighs = set(self.deployed_beacons[np.flatnonzero(self.prev_neigh_mask)])

            self.MIN.exploration_dir = self.get_exploration_dir_callback(self.MIN, self.neighs, np.zeros(2, ))
            self.__set_type_2_static_gains_optimistic()
            raise AtLandingConditionException
        return clamp(F, 4)

    def __get_force_type_1(self, xi_is):
        """Force created by potential field:
        U_{n+1, i} = (1/2)*k_i*norm(x_{n+1} - a_i*(x_i + xi_i*v_i))^2

        Returns:
            ndarray: total force acting on MIN from its neighbors
        """
        return -np.sum(
                self.neigh_mask*self.k_is*(self.MIN.pos.reshape(2, 1) - self.a_is*(self.beacon_x_is + xi_is*self.beacon_v_is))
            ,axis=1).reshape(2, )
    
    def __get_force_type_2(self, xi_is):
        """Force created by potential field:
        U_{n+1, i} = (1/2)*k_i*norm(x_{n+1} - (x_i + a_i*xi_i*v_i))^2

        Returns:
            ndarray: total force acting on MIN from its neighbors
        """
        return -np.sum(
                self.neigh_mask*self.k_is*(self.MIN.pos.reshape(2, 1) - (self.beacon_x_is + self.a_is*xi_is*self.beacon_v_is))
            ,axis=1).reshape(2, )

    def __get_type_1_dynamic_gains(self):

        k_is = np.ones(self.deployed_beacons.shape)

        # Using the fact that beacon at index i in self.deployed_beacons
        # has ID=i, to compute index of leader
        leader = np.argmax(np.flatnonzero(self.neigh_mask))

        a_is = np.zeros(self.deployed_beacons.shape)
        a_is[leader] = np.sum(self.neigh_mask)

        return k_is, a_is

    def __get_static_gains(self):
        return self.beacon_k_is, self.beacon_a_is

    def __set_type_2_static_gains(self):
        self.MIN.k = 1
        self.MIN.a = (2*self.D_BAR*(self.MIN.ID) + self.XI_BAR*np.sum([b.a for b in self.deployed_beacons]))/self.TAU_XI

    def __set_type_2_static_gains_optimistic(self):
        assert self.deployed_beacons[-1] in self.neighs, "ERROR! Previously deployed drone is not a neighbor"

        prev_deployed_beacon_neighs = self.deployed_beacons[-1].get_neighs()
        cluster = np.array(list(set().union(*([prev_deployed_beacon_neighs] + [r.get_neighs() for r in prev_deployed_beacon_neighs]))), dtype=object)
        
        cluster_k_is = [b.k for b in cluster]
        cluster_a_is = [b.a for b in cluster]

        self.MIN.k = 1 
        self.MIN.a = (2*self.D_BAR*self.MIN.ID  + self.XI_BAR*np.sum(cluster_a_is))

        print("cluster size: ", cluster.shape[0])
        
        