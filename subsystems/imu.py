from communication import network
from simulation import is_simulated

class IMU():
    def get_pitch(self):
        if is_simulated():
            return network["IMU/pitch"]
        else:
            return None

    def get_roll(self):
        if is_simulated():
            return network["IMU/roll"]
        else:
            return None

    def get_yaw(self):
        if is_simulated():
            return network["IMU/yaw"]
        else:
            return None

    def get_accel_x(self):
        if is_simulated():
            return network["IMU/accel_x"]
        else:
            return None

    def get_accel_y(self):
        if is_simulated():
            return network["IMU/accel_y"]
        else:
            return None

    def get_accel_z(self):
        if is_simulated():
            return network["IMU/accel_z"]
        else:
            return None
