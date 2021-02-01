import numpy as np
from helpers import (
    rot_z_mat as R_z,
    polar_to_vec as p2v
    )

class RangeReading():
    def __init__(self, measured_range):
        self.__measured_range = measured_range
        self.__is_valid = measured_range != np.inf
    
    def get_val(self):
        return np.array([self.__measured_range, 0, 0]).reshape(3, 1)
    
    def is_valid(self):
        return self.__is_valid

    def __str__(self):
        return f"Range reading: {self.__measured_range} [m]"

class RangeSensor():

    def __init__(self, max_range):
        self.max_range = max_range
        self.measurement = None

    def mount(self, host, angle_deg):
        self.host = host
        self.host_relative_angle = np.deg2rad(angle_deg)
        host.sensors.append(self)
        self.rot_mat = R_z(angle_deg)

    def sense(self, environment):
        self.measurement = RangeReading(
            np.min(np.concatenate(
                    [self.__sense_aux(corners) for corners in environment.obstacle_corners]
                )
            )
        )

    def __sense_aux(self, corners):
        """Computes the distance to an obstacle

        Args:
            corners ndarray: n-by-2 array representing the n corners of an obstacle as (x,  y)-coords. It is assumed that
            there is a line between the first and last corner defined in the array.

        Returns:
            float: distance along sensor-frame x-axis to nearest obstacle (inf if no obstacle is within range)
        """
        closed_corners = np.vstack((corners, corners[0, :]))
        valid_crossings = np.array([np.inf])
        A_1 = p2v(1, self.host_relative_angle + self.host.heading).reshape(2, 1)
        max_t = np.array([self.max_range, 1])
        for i in np.arange(corners.shape[0]):
            x1, x2 = closed_corners[i, :], closed_corners[i+1, :]

            A = np.hstack((A_1, (x1-x2).reshape(2, 1)))

            b = x1 - self.host.pos
            try:
                t = np.linalg.solve(A, b)
                if (t >= 0).all() and (t <= max_t).all():
                    valid_crossings = np.hstack((valid_crossings, t[0]))
            except np.linalg.LinAlgError:
                pass
        return valid_crossings
