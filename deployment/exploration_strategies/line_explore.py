from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)
from deployment.deployment_helpers import get_obstacle_forces as gof

import numpy as np

class LineExplore(ExplorationStrategy):
  def __init__(self, K_o=1, force_threshold=0.01, RSSI_threshold=0.1, ndims=1):
    self.K_o = K_o
    self.force_threshold = force_threshold
    self.RSSI_threshold = RSSI_threshold
    self.ndims = ndims

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    k_is = np.zeros(len(beacons))
    k_is[-1] = 1
    F = None
    if self.ndims == 1:
      """ 1D """
      x_is = np.array([b.pos[0] for b in beacons])
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])
      F = np.array([-np.sum(k_is*(MIN.pos[0] - x_is - RSSIs)), 0])
    elif self.ndims == 2:
      """ 2D """
      x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons], axis=1)
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])*np.ones((2, 1))
      F_n = -np.sum(k_is*(MIN.pos.reshape(2, 1) - x_is - RSSIs), axis=1).reshape(2, )
      F_o = gof(self.K_o, MIN, ENV)
      F = F_n + F_o
      #print(np.linalg.norm(F_o), np.linalg.norm(F))
    if np.linalg.norm(F) < self.force_threshold:
      raise AtLandingConditionException
    return F