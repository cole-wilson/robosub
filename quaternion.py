from pid import PID
from subsystems.imu import Quaternion, IMU
from simulation import network
import numpy as np

# from

x_pid = PID(3, 0, 0)
x_pid.set(0)
y_pid = PID(3, 0, 0)
y_pid.set(0)
z_pid = PID(3, 0, 0)
z_pid.set(0)

def quat_pid(imu: IMU, q_0: Quaternion, axis):
    print(q_0)
    if q_0 is None:
        return 0,0,0
    iq = imu.get_quaternion()
    if iq is None:
        return 0, 0, 0
    q_err = iq.inv() * q_0

    xd, yd, zd = (q_err.get_axis() - np.array(axis))

    x_t = -x_pid.calculate(xd)
    y_t = y_pid.calculate(yd)
    z_t = z_pid.calculate(zd)

    # network["debug_axes"] = {
    #     "start": q_err.get_axis().tolist(),
    #     "end": axis
    #     # "now": now_axis
    # }


    if axis[1]:
        return 0, y_t, z_t
    elif axis[0]:
        return x_t, 0, z_t
    elif axis[2]:
        return 0, y_t, z_t
    else:
        return y_t, x_t, z_t
#     print(network["debug_axes"])
