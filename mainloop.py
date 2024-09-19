from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.leds import LEDS
from subsystems.camera import Camera
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement
from scipy.spatial.transform import Rotation
import time

controller = Controller()
imu = IMU()
camera = Camera()
leds = LEDS(24)

#              (X,    Y,    Z)      (yaw, pitch)      min/max thrust
m1 = Thruster(-1.0, -1.0, -0.5,     -75,  00,     (-2.71, 3.48))
m2 = Thruster( 1.0, -1.0, -0.5,      75,  00,     (-2.71, 3.48))
m3 = Thruster(-1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48))
m4 = Thruster( 1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48))
m5 = Thruster(-1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20))
m6 = Thruster( 1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20))

motors = (m1, m2, m3, m4, m5, m6)

# once per boot
def setup():
    # keep next line for simulation
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement([0,0,0,0,0,0])

# every couple milliseconds when enabled
def loop():
    # leds.set_leds(0, 255, 0)
    expose_motors(m1, m2, m3, m4, m5, m6)

    leds.clear()
    leds.set_led(round(11 + (controller.getAxis(3) * -11)), 0, 255, 0)
    set_movement(get_movement(motors)) # keep for sim to work

    # m1.set_speed(controller.getAxis(3))

    # grav = 2

    y_speed = -20 * controller.getAxis(3)
    x_speed = 20 * controller.getAxis(2)
    pitch_speed = -1 * controller.getAxis(1)
    yaw_speed = -1 * controller.getAxis(0)


    z_speed = 0
    if controller.getButton(12):
        z_speed = 1
    elif controller.getButton(13):
        z_speed = -1

    roll_speed = 0
    if controller.getButton(4):
        roll_speed = -1
    elif controller.getButton(5):
        roll_speed = 1

    pool_oriented = False
    if pool_oriented:
        pool_oriented_speeds = [x_speed, y_speed, z_speed]
        pool_oriented_rot_speeds = [0, 0, yaw_speed]
        rotation = Rotation.from_euler("ZYX",[0, -imu.get_roll(), -imu.get_pitch()])
        x_speed, y_speed, z_speed = rotation.apply(pool_oriented_speeds)
        _, _, yaw_speed = rotation.apply(pool_oriented_rot_speeds)

    # sd = list(map(lambda i:round(i),[x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed]))

    motor_speeds = solve_motion(motors, x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed)["speeds"]

    for motor, speed in zip(motors, motor_speeds):
        motor.set_speed(speed)
    # m5.set_speed(y_speed)
    # m6.set_speed(y_speed)

# every couple milliseconds when disabled
def disabled():
    # print('loop')
    expose_motors(m1, m2, m3, m4, m5, m6)

    leds.set_leds(255, 0, 0)
    for motor in motors:
        motor.set_speed(0)
