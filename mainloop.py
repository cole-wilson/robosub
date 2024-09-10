from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement

controller = Controller()
imu = IMU()

#             X                   Y               Z                  yaw     pitch low speed high speed
FL = Thruster(-1,                 1,              0,                 0,      0,      (-2.71, 3.48))
FR = Thruster(1,                 1,              0,                  0,     0,      (-2.71, 3.48))
BR = Thruster(1,                 -1,              0,                 0,     0,      (-2.71, 3.48))
BL = Thruster(-1,                -1,              0,                 0,      0,      (-2.71, 3.48))
T1 = Thruster(-1,                 0,              0,                 0,      90,      (-6.40, 8.20))
T2 = Thruster(1,                 0,              0,                  0,      90,      (-6.40, 8.20))

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

    # get joystick axis:
    speed = controller.getAxis(1)
    FL.set_speed(speed * -5)

    print(imu.get_yaw())

    # solve for 6 motors speeds:
    # speeds = solve_motion(motors, Fx, Fy, Fz, Rx, Ry, Rz)


# every couple milliseconds when disabled
def disabled():
    for motor in motors:
        motor.set_speed(0)
