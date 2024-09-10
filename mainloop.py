from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement

controller = Controller()
imu = IMU()

#             X                   Y               Z                  yaw     pitch low speed high speed
FL = Thruster(0,                 -1.5,              0,               0,     90,     (-2.71, 3.48))
FR = Thruster(0,                 1.5,              0,                0,     90,     (-2.71, 3.48))
BR = Thruster(0,                 0,              -0.7,              -90,    0,      (-2.71, 3.48))
BL = Thruster(0,                0,              0.7,                 90,    0,      (-2.71, 3.48))
T1 = Thruster(-1,                 0,              0,                 0,     0,      (-6.40, 8.20))
T2 = Thruster(1,                 0,              0,                  0,     0,      (-6.40, 8.20))

motors = [FL, FR, BR, BL, T1, T2]

# once per boot
def setup():
    # keep next line for simulation
    expose_motors(*motors)

# every couple milliseconds when enabled
def loop():
    # keep these lines for simulation: ========
    movement = get_movement(motors)
    set_movement(movement)
    # =========================================

    grav =0# 2

    y_speed = -20 * controller.getAxis(3)
    x_speed = 5 * controller.getAxis(2)
    z_speed = -5 * controller.getAxis(1)

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

    yaw_speed = 0
    if controller.getButton(5):
        yaw_speed = 1
    elif controller.getButton(4):
        yaw_speed = -1
    # print(x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed)
    motor_speeds = solve_motion(motors, x_speed, y_speed, z_speed-grav, pitch_speed, roll_speed, yaw_speed)["speeds"]

    for motor, speed in zip(motors, motor_speeds):
        motor.set_speed(speed)

# every couple milliseconds when disabled
def disabled():
    for motor in motors:
        motor.set_speed(0)
