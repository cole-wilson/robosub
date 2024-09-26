from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.leds import LEDS
from subsystems.camera import Camera
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement
from scipy.spatial.transform import Rotation
import time
from simple_pid import PID

controller = Controller()
imu = IMU()
camera = Camera()
leds = LEDS(24)

roll_PID = PID(1, 0, 0, setpoint=0)
pitch_PID = PID(1, 0, 0, setpoint=0)
yaw_PID = PID(1, 0, 0, setpoint=0)

BUOYANCY = 2.5

def inch(inches):
    return 1.8 * (inches/10)


#              (X,    Y,    Z)      (yaw, pitch)      min/max thrust
# m1 = Thruster(-1.0, -1.0, -0.5,     -75,  00,     (-2.71, 3.48), 26)
# m2 = Thruster( 1.0, -1.0, -0.5,      75,  00,     (-2.71, 3.48), 20)
# m3 = Thruster(-1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48), 21)
# m4 = Thruster( 1.0,  0.0, -0.5,      00,  90,     (-2.71, 3.48), 22)
# m5 = Thruster(-1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20), 23)
# m6 = Thruster( 1.0,  1.0,  0.0,      00,  00,     (-6.40, 8.20), 24)

# m1 = Thruster(inch(-3), inch(0), inch(-2),     0,  -90,            (-2.71, 3.48), 20)
# m2 = Thruster(inch( 3), inch(0), inch(-2),     0,  -90,            (-2.71, 3.48), 21)
# m3 = Thruster(inch(0), inch(5.1875), inch(-3.375),     0,  00,     (-2.71, 3.48), 22)
# m4 = Thruster(inch(0), inch(5.1875), inch( 3.375),     0,  00,     (-2.71, 3.48), 23)
# m5 = Thruster(inch(-5.195), inch(3), inch(-0.5),     0,  00,       (-6.40, 8.20), 24)
# m6 = Thruster(inch( 5.195), inch(3), inch(-0.5),     0,  00,       (-6.40, 8.20), 26)

m1 = Thruster(-1, 0, -0.5,     0,  -90,            (-2.71, 3.48), 20)
m2 = Thruster(1, 0, -0.5,     0,  -90,            (-2.71, 3.48), 21)
m3 = Thruster(0,  1,   -1,     0,  00,     (-2.71, 3.48), 22)
m4 = Thruster(0,  1,   1,      0,  00,     (-2.71, 3.48), 23)
m5 = Thruster(-1,  0.5,   0,      0,   00,       (-6.40, 8.20), 24)
m6 = Thruster(1,   0.5,   0,     0,  00,       (-6.40, 8.20), 26)

motors = (m1, m2, m3, m4, m5, m6)

max_x = solve_motion(motors, 1000, 0, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][0]
max_y = solve_motion(motors, 0, 1000, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][1]
max_z = solve_motion(motors, 0, 0, 1000+BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][2]
max_pitch = solve_motion(motors, 0, 0, BUOYANCY, 1000, 0, 0, optimize=True, limit=True)["actual"][3]
max_roll = solve_motion(motors, 0, 0, BUOYANCY, 0, 1000, 0, optimize=True, limit=True)["actual"][4]
max_yaw = solve_motion(motors, 0, 0, BUOYANCY, 0, 0, 1000, optimize=True, limit=True)["actual"][5]

print(max_x, max_y, max_z, max_pitch, max_roll, max_yaw)

# once per boot
def setup():
    # keep next line for simulation
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement([0,0,0,0,0,0])

# every couple milliseconds when enabled
def loop():
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement(get_movement(motors))

    x_speed = max_x * controller.getAxis(2)
    y_speed = max_y * (controller.getButton(7) - controller.getButton(6))
    z_speed = max_z * (controller.getButton(0) - controller.getButton(2))
    yaw_speed = 3 * -controller.getAxis(0)
    pitch_speed = 3 * -controller.getAxis(1)
    roll_speed = controller.getButton(5) - controller.getButton(4)


    rotation = Rotation.from_euler("ZYX",[-imu.get_yaw(), -imu.get_roll(), -imu.get_pitch()])
    x_speed_b, y_speed_b, z_speed_b = rotation.apply([0, 0, BUOYANCY])

    # if y_speed > 22:
    #     controller.setRumble()
    # else:
    #     controller.stopRumble()
    # print(x_speed, y_speed, z_speed, pitch_speed, roll_speed, yaw_speed)

    if abs(roll_speed) < 0.1 and abs(pitch_speed) < 0.1 and abs(yaw_speed) < 0.1:
        roll_speed = roll_PID(imu.get_roll())
        pitch_speed = pitch_PID(imu.get_pitch())
        yaw_speed = yaw_PID(imu.get_yaw())
    else:
        roll_PID.setpoint = imu.get_roll()
        pitch_PID.setpoint = imu.get_pitch()
        yaw_PID.setpoint = imu.get_yaw()

    motor_speeds = solve_motion(motors, x_speed - x_speed_b, y_speed - y_speed_b, z_speed - z_speed_b, pitch_speed, roll_speed, yaw_speed)["speeds"]

    for motor, speed in zip(motors, motor_speeds):
        motor.set_speed(speed)


    # print(round(m6.speed - m5.speed), round(m3.speed - m4.speed))

# every couple milliseconds when disabled
def disabled():
    # print('loop')
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement([0,0,0,0,0,0])

    leds.set_leds(255, 0, 0)
    for motor in motors:
        motor.set_speed(0)
