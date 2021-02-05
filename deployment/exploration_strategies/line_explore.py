from deployment.exploration_strategies.exploration_strategy import (
    ExplorationStrategy,
    AtLandingConditionException
)

import numpy as np

class LineExplore(ExplorationStrategy):
  def __init__(self, force_threshold=0.001, RSSI_threshold=0.1):
    self.force_threshold = force_threshold
    self.RSSI_threshold = RSSI_threshold

  def prepare_exploration(self, target):
      return super().prepare_exploration(target)

  def get_exploration_velocity(self, MIN, beacons, ENV):
    x_is = np.array([b.pos[0] for b in beacons])
    RSSIs = np.array([MIN.get_RSSI(b) for b in beacons])
    k_is = np.zeros(len(beacons))
    k_is[-1]=10
    F = -np.sum(k_is*(MIN.pos[0] - x_is - RSSIs))
    if np.linalg.norm(F) < self.force_threshold:
      x_star = np.sum(k_is*(x_is + RSSIs))/np.sum(k_is)
      print(x_star, MIN.pos[0])
      raise AtLandingConditionException
    return np.array([F, 0])