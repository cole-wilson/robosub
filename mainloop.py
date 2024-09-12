from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.leds import LEDS
from subsystems.camera import Camera
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement
from scipy.spatial.transform import Rotation

controller = Controller()
imu = IMU()
camera = Camera()
print(333)
leds = LEDS(128)
print(111)

#              (X,    Y,    Z)      (yaw, pitch)      min/max thrust
m1 = Thruster(-1.0, -1.0, -0.5,     -75,  00,     (-2.71, 3.48))
m2 = Thruster( 1.0, -1.0, -0.5,      75,  00,     (-2.71, 3.48))
m3 = Thruster(-1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48))
m4 = Thruster( 1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48))
m5 = Thruster(-1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20))
m6 = Thruster( 1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20))

motors = [m1, m2, m3, m4, m5, m6]

# once per boot
def setup():
    # keep next line for simulation
    expose_motors(m1, m2, m3, m4, m5, m6)

# every couple milliseconds when enabled
def loop():
    # print(1)
    leds.set_leds(0, 255, 0)
    set_movement(get_movement(motors)) # keep for sim to work

    grav = 2

    y_speed = -5 * controller.getAxis(3)
    x_speed = 5 * controller.getAxis(2)
    z_speed = -5 * controller.getAxis(1)
    yaw_speed = -1 * controller.getAxis(0)


    # hello brady

    pool_oriented_speeds = [x_speed, y_speed, z_speed]
    rotation = Rotation.from_euler("ZYX",[0, -imu.get_roll(), -imu.get_pitch()])
    x_speed, y_speed, z_speed = rotation.apply(pool_oriented_speeds)
    # z_speed -= imu.get_accel_z()
    # print(imu.get_accel_z())
    # yaw_speed = 5 * controller.getAxis(2)

    pitch_speed = 0
    if controller.getButton(12):
        pitch_speed = 1
    elif controller.getButton(13):
        pitch_speed = -1

    roll_speed = 0
    if controller.getButton(14):
        roll_speed = -1
    elif controller.getButton(15):
        roll_speed = 1

    # yaw_speed = 0
    # if controller.getButton(5):
    #     yaw_speed = 1
    # elif controller.getButton(4):
    #     yaw_speed = -1



    # print(x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed)
    motor_speeds = solve_motion(motors, x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed)["speeds"]

    for motor, speed in zip(motors, motor_speeds):
        motor.set_speed(speed)

# every couple milliseconds when disabled
def disabled():
    leds.set_leds(255, 0, 0)
    for motor in motors:
        motor.set_speed(0)
