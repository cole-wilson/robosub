from communication import network
from simulation import is_simulated
import math
from scipy.spatial.transform import Rotation

if not is_simulated():
    # # import board
    # import serial
    # # import busio
    # import adafruit_bno055
    import board
    import busio
    import adafruit_bno055


class Quaternion():
    x = y = z = w = None

    def __init__(self, w=1, x=0, y=0, z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def scalar_first(self):
        return [self.w, self.x, self.y, self.z]

    def scalar_last(self):
        return [self.x, self.y, self.z, self.w]

    @classmethod
    def from_BNO055(cls, sensor_quat):
        q = cls(sensor_quat[])


class IMU():
    sensor = None

    def __init__(self) -> None:
        ...
        if not is_simulated():
            # i2c = busio.I2C(board.SCL, board.SDA)
            # sensor = adafruit_bno055.BNO055_I2C(i2c)
            # i2c = busio.I2C(board.SCL, board.SDA)
            # sensor = adafruit_bno055.BNO055_I2C(i2c)
            try:
                self.i2c = busio.I2C(board.SCL, board.SDA)
                # self.uart = serial.Serial("/dev/serial0")
                # self.sensor = adafruit_bno055.BNO055_UART(self.uart)
                self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
                # for i in range(100):
                    # print(self.sensor.axis_remap)
            except:
                pass

    def get_quaternion(self):
        if is_simulated() or not self.sensor:
            quat = network["IMU/quaternion"] or None
            # print(quat)
            if quat is None:
                return None
            quat_py = [
                -quat[0],
                quat[1],
                quat[2],
                quat[3]
            ]
            return quat_py
        else:
            # rot = Rotation.from_quat(self.sensor.quaternion)
            # rot.
            q_sens = self.sensor.quaternion
            if q_sens is None or q_sens[0] is None:
                return None
            quat = [
                q_sens[1],
                q_sens[2],
                q_sens[3],
                q_sens[0]
            ]
            quat_py = [
                -q_sens[1],
                q_sens[2],
                q_sens[3],
                q_sens[0]
            ]
            network["IMU/quaternion"] = quat
            return quat_py

    # def get_pitch(self):
    #     if is_simulated() or not self.sensor:
    #         return network["IMU/pitch"] or 0
    #     else:
    #         network["IMU/pitch"] = -math.radians(self.sensor.euler[2] or 0)
    #         return -math.radians(self.sensor.euler[2] or 0)

    # def get_roll(self):
    #     if is_simulated() or not self.sensor:
    #         return network["IMU/roll"] or 0
    #     else:
    #         network["IMU/roll"] = -math.radians(self.sensor.euler[1] or 0)
    #         return -math.radians(self.sensor.euler[1] or 0)

    # def get_yaw(self):
    #     if is_simulated() or not self.sensor:
    #         return network["IMU/yaw"] or 0
    #     else:
    #         network["IMU/yaw"] = -math.radians(self.sensor.euler[0] or 0)
    #         return -math.radians(self.sensor.euler[0] or 0)
    def get_accel_x(self):
        if is_simulated() or not self.sensor:
            return network["IMU/accel_x"] or 0
        else:
            ax = self.sensor.linear_acceleration[0]
            network["IMU/accel_x"] = ax
            return ax

    def get_accel_y(self):
        if is_simulated() or not self.sensor:
            return network["IMU/accel_y"] or 0
        else:
            ay = self.sensor.linear_acceleration[1]
            network["IMU/accel_y"] = ay
            return ay

    def get_accel_z(self):
        if is_simulated() or not self.sensor:
            return network["IMU/accel_z"] or 0
        else:
            az = self.sensor.linear_acceleration[2]
            network["IMU/accel_z"] = az
            return az
