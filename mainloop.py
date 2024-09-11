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
leds = LEDS(128)

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
    leds.set_leds(0, 255, 0)
    set_movement(get_movement(motors)) # keep for sim to work

    # get joystick axis:
    speed = controller.getAxis(1)
    m1.set_speed(speed * -5)

    print("Yaw is:", imu.get_yaw())

    # solve for 6 motors speeds:
    # speeds = solve_motion(motors, Fx, Fy, Fz, Rx, Ry, Rz)

    # read a capture/image from the camera
    # ret, cap = camera.read()

# every couple milliseconds when disabled
def disabled():
    leds.set_leds(255, 0, 0)
    for motor in motors:
        motor.set_speed(0)
