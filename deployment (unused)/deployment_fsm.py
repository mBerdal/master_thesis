from beacons.MIN.min import MinState
from deployment.following_strategies.following_strategy import AtTargetException
from deployment.exploration_strategies.exploration_strategy import AtLandingConditionException
from numpy import zeros

class DeploymentFSM():

    def __init__(self, following_strategy, exploration_strategy):
        self.fs = following_strategy
        self.es = exploration_strategy

    def get_velocity_vector(self, MIN, beacons, SCS, ENV):
        if MIN.state == MinState.SPAWNED:
            self.fs.prepare_following(MIN, beacons, SCS)
            MIN.state = MinState.FOLLOWING
        if MIN.state == MinState.FOLLOWING:
            try:
                return self.fs.get_following_velocity(MIN, beacons, ENV)
            except AtTargetException:
                self.es.prepare_exploration(self.fs.target)
                MIN.state = MinState.EXPLORING
                print(f"{MIN.ID} exploring")
        if MIN.state == MinState.EXPLORING:
            try:
                return self.es.get_exploration_velocity(MIN, beacons, ENV)
            except AtLandingConditionException:
                MIN.state = MinState.LANDED
                return zeros((2, ))
        else:
            print("MIN ALREADY LANDED")
            exit(0)
    
    def get_target(self):
        return self.fs.target