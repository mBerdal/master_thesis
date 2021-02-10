from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)
from deployment.deployment_helpers import get_obstacle_forces as gof

import numpy as np
from enum import Enum

class LineExploreKind(Enum):
      ONE_DIM_TYPE_1 = 1,
      ONE_DIM_TYPE_2 = 2,
      TWO_DIM        = 3,

class LineExplore(ExplorationStrategy):
  def __init__(self, K_o=1, force_threshold=0.01, RSSI_threshold=0.5, kind=LineExploreKind.ONE_DIM_TYPE_1):
    self.K_o = K_o
    self.force_threshold = force_threshold
    self.RSSI_threshold = RSSI_threshold
    self.kind = kind

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    F, F_n, F_o = None, None, None

    if self.kind != LineExploreKind.TWO_DIM:
      """ 1D """
      tmp_RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])

      neigh_indices, = np.where(tmp_RSSIs > self.RSSI_threshold)
      n_neighs = len(neigh_indices)

      RSSIs = tmp_RSSIs[neigh_indices]
      x_is = np.array([b.pos[0] for b in beacons[neigh_indices]])
      if self.kind == LineExploreKind.ONE_DIM_TYPE_1:
        k_is = np.array([(i+1)**4 for i in range(n_neighs)])
        F_n = -np.sum(k_is*(MIN.pos[0] - (x_is + RSSIs)))
      elif self.kind == LineExploreKind.ONE_DIM_TYPE_2:
        k_is = np.ones(x_is.shape)
        a_is = np.array([
          (1/2)**i for i in range(n_neighs, 0, -1)
        ])
        F_n = -np.sum(k_is*(MIN.pos[0] - a_is*(x_is + RSSIs)))

      F_o = 0*gof(self.K_o, MIN, ENV)[0]
      F = np.array([F_n + F_o, 0])
      if n_neighs == 0:
            print("STOPPED due to no neighs")
    else:
      """ 2D """
      k_is = np.zeros(len(beacons))
      k_is[-1] = 1
      x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons], axis=1)
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])*np.ones((2, 1))
      F_n = -np.sum(k_is*(MIN.pos.reshape(2, 1) - x_is - RSSIs), axis=1).reshape(2, )
      F_o = gof(self.K_o, MIN, ENV)
      F = F_n + F_o
          
    if np.linalg.norm(F) < self.force_threshold:
      raise AtLandingConditionException
    return F