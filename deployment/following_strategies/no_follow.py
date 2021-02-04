from deployment.following_strategies.following_strategy import FollowingStrategy, AtTargetException

class NoFollow(FollowingStrategy):

  def __init__(self):
    pass

  def prepare_following(self, MIN, beacons, SCS):
    pass

  def get_following_velocity(self, MIN, ENV):
      raise AtTargetException