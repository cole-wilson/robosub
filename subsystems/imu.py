from communication import network
from simulation import is_simulated
import math
from scipy.spatial.transform import Rotation
import numpy as np
from typing import Self

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

    def as_wxyz(self) -> tuple:
        return (self.w, self.x, self.y, self.z)

    def as_xyzw(self) -> tuple:
        return (self.x, self.y, self.z, self.w)

    def as_rotation(self) -> Rotation:
        return Rotation.from_quat([-self.x, self.y, self.z, self.w])

    def inv(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def get_axis(self):
        return np.array([self.x, self.y, self.z])

    @classmethod
    def from_xyzw(cls, arr:list) -> Self:
        x = arr[0]
        y = arr[1]
        z = arr[2]
        w = arr[3]
        return cls(w, x, y, z)

    @classmethod
    def from_BNO055(cls, sensor_quat) -> Self:
        return cls(*sensor_quat)

    def times(self, q) -> Self:
        p = self
        p0 = p.w
        q0 = q.w

        P = np.array([p.x, p.y, p.z])
        Q = np.array([q.x, q.y, q.z])

        pq_w = (p0 * q0) - np.dot(P, Q)
        pq_xyz = (p0 * Q) + (q0 * P) + np.cross(P, Q)
        return Quaternion(pq_w, *pq_xyz)

    def __mul__(self, other):
        return self.times(other)

    @classmethod
    def from_euler(cls, roll, pitch, yaw):
        # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        cr = math.cos(roll * 0.5);
        sr = math.sin(roll * 0.5);
        cp = math.cos(pitch * 0.5);
        sp = math.sin(pitch * 0.5);
        cy = math.cos(yaw * 0.5);
        sy = math.sin(yaw * 0.5);

        w = cr * cp * cy + sr * sp * sy;
        x = sr * cp * cy - cr * sp * sy;
        y = cr * sp * cy + sr * cp * sy;
        z = cr * cp * sy - sr * sp * cy;

        return cls(w, x, y, z)

    def __repr__(self):
        return f"<<{round(self.w, 3)}, {round(self.x, 3)}, {round(self.y, 3)}, {round(self.z, 3)}>>"



class IMU():
    sensor = None

    def __init__(self) -> None:
        if not is_simulated():
            try:
                self.i2c = busio.I2C(board.SCL, board.SDA)
                # self.uart = serial.Serial("/dev/serial0")
                # self.sensor = adafruit_bno055.BNO055_UART(self.uart)
                self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
                # for i in range(100):
                    # print(self.sensor.axis_remap)
            except Exception as e:
                print("imu error", e)
                pass

    def get_quaternion(self) -> Quaternion:
        if is_simulated() or not self.sensor:
            quat = network["IMU/quaternion"] or None
            if quat is not None:
                return Quaternion.from_xyzw(network["IMU/quaternion"])
        else:
            q_sens = self.sensor.quaternion
            if q_sens is None or q_sens[0] is None:
                print("missing IMU!!!")
                return None

            q = Quaternion.from_BNO055(q_sens)
            network["IMU/quaternion"] = q.as_xyzw()
            return q

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
