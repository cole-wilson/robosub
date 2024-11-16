from subsystems.controller import Controller
from subsystems.imu import IMU
from subsystems.leds import LEDS
from subsystems.camera import Camera
from subsystems.servo import Servo
from subsystems.digitalinput import DigitalInput
from subsystems.thruster import Thruster, get_movement, solve_motion
from simulation import expose_motors, set_movement
from pid import PID
import cv2
from scipy.spatial.transform import Rotation
import time

controller = Controller()
imu = IMU()
camera = Camera()
leds = LEDS(18, n=89)

roll_PID = PID(4, 0, 0, setpoint=0)
pitch_PID = PID(4, 0, 0, setpoint=0)
yaw_PID = PID(4, 0, 0, setpoint=0)

BUOYANCY = 1

def inch(inches):
    return 1.8 * (inches/10)

m1 = Thruster(-1, 0, -0.5,     0,  -90,            (-2.71, 3.48), 9)
m2 = Thruster(1, 0, -0.5,     0,  -90,            (-2.71, 3.48), 11)
m3 = Thruster(0,  1,   -1,     0,  00,     (-2.71, 3.48), 19)
m4 = Thruster(0,  1,   1,      0,  00,     (-2.71, 3.48), 26)
m5 = Thruster(-1,  0.5,   0,      0,   00,       (-6.40, 8.20), 16)
m6 = Thruster(1,   0.5,   0,     0,  00,       (-6.40, 8.20), 20)
motors = (m1, m2, m3, m4, m5, m6)

panServo = Servo(23)
tiltServo = Servo(24)
moisture = DigitalInput(1, default=0)

max_x = solve_motion(motors, 1000, 0, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][0]
min_x = solve_motion(motors, -1000, 0, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][0]
max_y = solve_motion(motors, 0, 1000, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][1]
min_y = solve_motion(motors, 0, -1000, BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][1]
max_z = solve_motion(motors, 0, 0, 1000+BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][2]
min_z = solve_motion(motors, 0, 0, -1000+BUOYANCY, 0, 0, 0, optimize=True, limit=True)["actual"][2]
max_pitch = solve_motion(motors, 0, 0, BUOYANCY, 1000, 0, 0, optimize=True, limit=True)["actual"][3]
max_roll = solve_motion(motors, 0, 0, BUOYANCY, 0, 1000, 0, optimize=True, limit=True)["actual"][4]
max_yaw = solve_motion(motors, 0, 0, BUOYANCY, 0, 0, 1000, optimize=True, limit=True)["actual"][5]

# once per boot
def setup():
    # keep next line for simulation
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement([0,0,0,0,0,0])

# every couple milliseconds when enabled
def enabled():
    # _, cap = camera.read()
    # cv2.imshow("a", cap)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement(get_movement(motors))

    x_speed = max_x * controller.getAxis(2)
    y_speed = (max_y * controller.getButton(7)) + (min_y * controller.getButton(6))
    z_speed = (max_z * controller.getButton(0)) + (min_z * controller.getButton(2))

    yaw_speed = 3 * -controller.getAxis(0)
    pitch_speed = 3 * -controller.getAxis(1)
    roll_speed = controller.getButton(5) - controller.getButton(4)


    # for i in range():
    leds.clear()
    leds.set_led(44 + round(44*(controller.getButton(7) - controller.getButton(6))), 0,255,0)

    quat = imu.get_quaternion()
    if quat is not None:
        try:
            rotation = Rotation.from_quat(quat)
            # print(rotation)

            x_speed_b, y_speed_b, z_speed_b = rotation.apply([0, 0, BUOYANCY])
            # print(x_speed_b, y_speed_b, z_speed_b)
        except Exception as e:
            print('excp', e)
            x_speed_b, y_speed_b, z_speed_b = (0, 0, 0)
    else:
        x_speed_b, y_speed_b, z_speed_b = (0, 0, 0)


    if y_speed > max_y - 0.5:
        controller.setRumble()
    else:
        controller.stopRumble()

    motor_speeds = solve_motion(motors, x_speed - x_speed_b, y_speed - y_speed_b, z_speed - z_speed_b, pitch_speed, roll_speed, yaw_speed)["speeds"]


    for motor, speed in zip(motors, motor_speeds):
        motor.set_speed(speed)
    print([imu.get_accel_x(), imu.get_accel_y(), imu.get_accel_z()])


# every couple milliseconds when disabled
def disabled():
    # print('disabled')
    # [imu.get_yaw(), imu.get_roll(), imu.get_pitch()]
    [imu.get_accel_x(), imu.get_accel_y(), imu.get_accel_z()]
    imu.get_quaternion()
    # print('loop')
    expose_motors(m1, m2, m3, m4, m5, m6)
    set_movement([0,0,0,0,0,0])

    leds.set_leds(255,  0, 0)
    for motor in motors:
        motor.set_speed(0)
