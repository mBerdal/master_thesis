from deployment.following_strategies.following_strategy import FollowingStrategy
from helpers import normalize

class StraightLineFollow(FollowingStrategy):
    
    def prepare_following(self, MIN, beacons, SCS):
        super().prepare_following(MIN, beacons, SCS)
        self.beacons_to_follow = [self.target]
        self.compute_next_beacon_to_follow()

    @FollowingStrategy.follow_velocity_wrapper
    def get_following_velocity(self, MIN, beacons, ENV):
        return self.MAX_FOLLOWING_SPEED*normalize(MIN.get_vec_to_other(self.btf))