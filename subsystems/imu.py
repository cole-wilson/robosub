from communication import network
from simulation import is_simulated
import math

if not is_simulated():
    # # import board
    # import serial
    # # import busio
    # import adafruit_bno055
    import board
    import busio
    import adafruit_bno055


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
            except:
                pass

    def get_pitch(self):
        if is_simulated() or not self.sensor:
            return network["IMU/pitch"] or 0
        else:
            network["IMU/pitch"] = -math.radians(self.sensor.euler[2] or 0)
            return -math.radians(self.sensor.euler[2] or 0)

    def get_roll(self):
        if is_simulated() or not self.sensor:
            return network["IMU/roll"] or 0
        else:
            network["IMU/roll"] = -math.radians(self.sensor.euler[1] or 0)
            return -math.radians(self.sensor.euler[1] or 0)

    def get_yaw(self):
        if is_simulated() or not self.sensor:
            return network["IMU/yaw"] or 0
        else:
            network["IMU/yaw"] = -math.radians(self.sensor.euler[0] or 0)
            return -math.radians(self.sensor.euler[0] or 0)

    def get_accel_x(self):
        if is_simulated():
            return network["IMU/accel_x"] or 0
        else:
            return None

    def get_accel_y(self):
        if is_simulated():
            return network["IMU/accel_y"] or 0
        else:
            return None

    def get_accel_z(self):
        if is_simulated():
            return network["IMU/accel_z"] or 0
        else:
            return None
