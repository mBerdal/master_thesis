import numpy as np

class RangeReading():
    def __init__(self, measured_range):
        self.__measured_range = measured_range
    
    def get_val(self):
        return self.__measured_range

    def __str__(self):
        return f"Range reading: {self.__measured_range} [m]"

class RangeSensor():

    def __init__(self, max_range):
        self.max_range = max_range

    def mount(self, host, angle_deg):
        self.host = host
        host.sensors.append(self)
        self.host_relative_angle = np.deg2rad(angle_deg)

    def sense(self, environment):
        abs_angle = self.host_relative_angle + np.arctan2(self.host.heading[1], self.host.heading[0])
        closed_corners = np.vstack((environment.corners, environment.corners[0, :]))
        valid_crossings = np.array([np.inf])
        max_t = np.array([self.max_range, 1])
        for i in np.arange(environment.corners.shape[0]):
            x1, x2 = closed_corners[i, :], closed_corners[i+1, :]

            A = np.array([
                [np.cos(abs_angle), x1[0]-x2[0]],
                [np.sin(abs_angle), x1[1]-x2[1]]
            ])
            b = x1 - self.host.pos
            try:
                t = np.linalg.solve(A, b)
                if (t >= 0).all() and (t <= max_t).all():
                    valid_crossings = np.hstack((valid_crossings, t[0]))
            except np.linalg.LinAlgError:
                pass
        return RangeReading(np.min(valid_crossings))
