from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)

import numpy as np

class LineExplore(ExplorationStrategy):
  def __init__(self, force_threshold=0.01):
    self.force_threshold = force_threshold

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    x_is = np.array([b.pos[0] for b in beacons])
    RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])
    k_is = np.ones(len(beacons))
    F = np.sum(k_is*(MIN.pos[0] - x_is - RSSIs))
    if F < self.force_threshold:
      raise AtLandingConditionException
    return np.array([F, 0])