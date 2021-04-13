import numpy as np
from helpers import (
    rot_z_mat as R_z,
    polar_to_vec as p2v
    )


class RangeReading():
    def __init__(self, measured_range):
        self.__measured_range = measured_range
    
    def get_3d_range_vec(self):
        return np.array([self.__measured_range, 0, 0]).reshape(3, 1)
    
    def get_2d_range_vec(self):
        return np.array([self.__measured_range, 0]).reshape(2, 1)

    def get_range(self):
        return self.__measured_range

    def __str__(self):
        return f"Range reading: {self.__measured_range} [m]"


class RangeSensor():

    def __init__(self, max_range):
        self.max_range = max_range
        self.measurement = None

    def mount(self, host, angle_deg):
        self.host = host
        self.host.sensors.append(self)
        self.host_relative_angle = np.deg2rad(angle_deg)
        self.rot_mat = R_z(angle_deg)

    def sense(self, environment):
        if environment.obstacle_corners == []:
          self.measurement = RangeReading(self.max_range)
        else:
            self.measurement = RangeReading(self.__sense_aux(environment.list_of_segments))

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
