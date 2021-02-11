from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)
from deployment.deployment_helpers import get_obstacle_forces as gof

import numpy as np
from enum import Enum

class LineExploreKind(Enum):
      ONE_DIM_LOCAL  = 1,
      ONE_DIM_GLOBAL = 2,
      TWO_DIM_GLOBAL = 3,

class LineExplore(ExplorationStrategy):
  def __init__(self, K_o=1, force_threshold=0.01, RSSI_threshold=0.5, kind=LineExploreKind.ONE_DIM_GLOBAL):
    self.K_o = K_o
    self.force_threshold = force_threshold
    self.RSSI_threshold = RSSI_threshold
    self.kind = kind

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    F, F_n, F_o = None, None, None

    if self.kind != LineExploreKind.TWO_DIM_GLOBAL:
      """ 1D """
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])
      x_is = np.array([b.pos[0] for b in beacons])
      k_is, a_is = None, None

      if self.kind == LineExploreKind.ONE_DIM_GLOBAL:
        k_is = np.ones(x_is.shape)
        a_is = np.ones(x_is.shape)
        a_is[-1] = 1 + (1/k_is[-1])*np.sum(k_is[:-1])
        assert k_is[-1]*(a_is[-1] - 1) >= np.sum(k_is[:-1]) and a_is[-1] >= 0,\
           "Conditions on constants a_i and k_i do not hold. Cannot guarantee x_n_plus_one > x_n"

      elif self.kind == LineExploreKind.ONE_DIM_LOCAL:
        neigh_indices, = np.where(RSSIs > self.RSSI_threshold)
        n_neighs = len(neigh_indices)
        if n_neighs == 0:
            print("STOPPED due to no neighs")
        
        x_is = x_is[neigh_indices]
        RSSIs = RSSIs[neigh_indices]

        k_is = np.ones(x_is.shape)
        a_is = np.ones(x_is.shape)

        j = np.argmax(x_is)
        a_is[j] = 1 + (1/k_is[j])*np.sum(np.delete(k_is, j))

        assert k_is[j]*(a_is[j] - 1) >= np.sum(np.delete(k_is, j)) and a_is[j] >= 0,\
           "Conditions on constants a_i and k_i do not hold. Cannot guarantee x_n_plus_one > max(x_i) for i in neighbors of nu_n_plus_one"
        
      F_n = -np.sum(k_is*(MIN.pos[0] - a_is*(x_is + RSSIs)))
      F_o = 0*gof(self.K_o, MIN, ENV)[0]
      F = np.array([F_n + F_o, 0])
      
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