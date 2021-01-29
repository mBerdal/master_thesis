from abc import ABC, abstractmethod

class DeploymentStrategy(ABC):


    @abstractmethod
    def follow(self, MIN, beacons, SCS, ENV, following_strategy):
        pass

    @abstractmethod
    def explore(self, MIN, beacons, ENV):
        pass

    @abstractmethod
    def get_heading_and_speed(self, MIN, beacons, SCS, ENV):
        pass