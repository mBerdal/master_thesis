from deployment.exploration_strategies.exploration_strategy import (
    AtLandingConditionException
)
from deployment.deployment_helpers import get_obstacle_forces as gof

import numpy as np

class LineDeploy():

  TAU_XI = 0.5

  def __init__(self, force_threshold=0.01, get_exploration_dir_callback = lambda MIN, neighs: np.array([1, 0])):
    self.neigh_idxs = None
    self.prev_neigh_idx_set = set()
    self.__force_thresh = force_threshold
    self.__get_v = get_exploration_dir_callback

  def get_velocity_vector(self, MIN, beacons, SCS, ENV):
    xi_is = np.array([MIN.get_xi_to_other_from_model(b) for b in beacons])

    self.neigh_idxs = np.argwhere(xi_is >= self.TAU_XI).reshape(-1)
    self.neigh_xi_is = xi_is[self.neigh_idxs]
    neighs_idx_set = set(self.neigh_idxs)

    if not neighs_idx_set == self.prev_neigh_idx_set:
      self.prev_neigh_idx_set = neighs_idx_set

      self.neigh_x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons[self.neigh_idxs]], axis=1)
      self.neigh_v_is = np.concatenate([b.v.reshape(2, 1) for b in beacons[self.neigh_idxs]], axis=1)

      leader_idx = np.argmax([b.ID for b in beacons[self.neigh_idxs]])

      self.neigh_k_is = np.ones(self.neigh_idxs.shape)
      self.neigh_a_is = np.zeros(self.neigh_idxs.shape)
      self.neigh_a_is[leader_idx] = np.sum(self.neigh_k_is)

    F = -np.sum(
      self.neigh_k_is*(
        MIN.pos.reshape(2, 1) - self.neigh_a_is*(self.neigh_x_is + self.neigh_xi_is*self.neigh_v_is)
      )
    , axis=1).reshape(2, )

    if np.linalg.norm(F) < self.__force_thresh and self.neigh_idxs.shape[0] != 0:
      MIN.v = self.__get_v(MIN, beacons[self.neigh_idxs])
      raise AtLandingConditionException
    elif self.neigh_idxs.shape[0] == 0:
      print(f"MIN {MIN.ID} landing due to no neighbors")
      MIN.v = self.__get_v(MIN, beacons[np.array(self.prev_neigh_idx_set)])
      raise AtLandingConditionException 

    return F

