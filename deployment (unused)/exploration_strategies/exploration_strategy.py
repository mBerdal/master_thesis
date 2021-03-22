from abc import ABC, abstractmethod
import numpy as np

class ExplorationStrategy(ABC):

    MAX_EXPLORATION_SPEED = 2
    MIN_RSSI_STRENGTH_BEFORE_LAND = np.exp(-2.9)

    def prepare_exploration(self, target):
        self.target = target
        
    @abstractmethod
    def get_exploration_velocity(self, MIN, beacons, ENV):
        pass