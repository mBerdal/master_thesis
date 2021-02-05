from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)

import numpy as np

class LineExplore(ExplorationStrategy):
  def __init__(self, force_threshold=0.001, RSSI_threshold=0.1, ndims=1):
    self.force_threshold = force_threshold
    self.RSSI_threshold = RSSI_threshold
    self.ndims = ndims

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    k_is = np.ones(len(beacons))
    if self.ndims == 1:
      """ 1D """
      x_is = np.array([b.pos[0] for b in beacons])
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])
      F = np.array([-np.sum(k_is*(MIN.pos[0] - x_is - RSSIs)), 0])
    elif self.ndims == 2:
      """ 2D """
      x_is = np.concatenate([b.pos.reshape(2, 1) for b in beacons], axis=1)
      RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])*np.ones((2, 1))
      F = -np.sum(k_is*(MIN.pos.reshape(2, 1) - x_is - RSSIs), axis=1).reshape(2, 1)
    if np.linalg.norm(F) < self.force_threshold:
      raise AtLandingConditionException
    return F