import numpy as np
from helpers import (
    rot_z_mat as R_z,
    polar_to_vec as p2v
    )

class RangeSensor():

    def __init__(self, max_range):
        self.max_range = max_range
        self.measurement = None

    def mount(self, host, angle_deg):
        self.host = host
        self.host.sensors.append(self)
        self.host_relative_angle = np.deg2rad(angle_deg)

    def get_measurement(self, environment):
        return self.__sense_aux(environment.list_of_segments), self.host.heading + self.host_relative_angle

    def __sense_aux(self, list_of_segments):
        """Computes the distance to an obstacle

        Args:
            list_of_segments list: list of Segment objects corresponding to walls in the environment.

        Returns:
            float: distance along sensor-frame x-axis to nearest obstacle (inf if no obstacle is within range)
        """

        b = p2v(1, self.host_relative_angle + self.host.heading)
        sensed_ranges = self.max_range*np.ones((1, ))
        
        for seg in list_of_segments:
            crs = np.cross(seg.vec, b)
            if not crs == 0:
                v = (self.host.pos - seg.start) / crs
                t = np.cross(v, b)
                sensed_range = np.cross(v, seg.vec)
                if 0 <= t and t <= 1 and 0 <= sensed_range and sensed_range <= self.max_range:
                    sensed_ranges = np.concatenate((sensed_ranges, [sensed_range]))
        return np.min(sensed_ranges)
