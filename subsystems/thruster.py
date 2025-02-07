import numpy as np
from math import sin, cos, tan, radians
from scipy.optimize import minimize, lsq_linear
import time
import functools

import simulation

if not simulation.is_simulated():
    import pigpio
    pi = pigpio.pi()       # pi1 accesses the local Pi's GPIO
    # import RPi.GPIO as GPIO
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)

np.set_printoptions(precision=3, suppress=True)

def in_to_ft(x):
    return (1/12.0) * x

# def calculate_duty_cycle(pulse_width, frequency):
    # return (pulse_width / (1/))

class Thruster():
    speed = 0
    pin = None
    maxthrust = 0

    def __init__(self, x, y, z, theta, phi, speed_bounds = (-0.7, 1), pinBCM=None, freq=400):
        if pinBCM and not simulation.is_simulated():
            self.pin = pinBCM
            pi.set_servo_pulsewidth(self.pin, 1500)
            time.sleep(0.3)
        self.x = x
        self.y = y
        self.z = z
        self.phi = phi
        self.theta = theta
        self.speedbound_reverse, self.speedbound_forward = speed_bounds

    def stop(self):
        if self.pin:
            pi.set_servo_pulsewidth(self.pin, 1500)


    def get_force_coefficients(self):
        p = radians(90-self.phi)
        t = radians(90+self.theta)

        sinp = sin(p)
        sint = sin(t)
        cost = cos(t)
        cosp = cos(p)

        # input(sinp * cost)

        return [
            sinp * cost,
            sinp * sint,
            cosp
        ]

    def set_speed(self, speed):
        self.speed = speed
        throttle = 0
        if self.pin:
            if speed < 0:
                throttle = -speed/self.speedbound_reverse
            else:
                throttle = speed/self.speedbound_forward

            # print(throttle)
            if throttle > self.maxthrust:
                self.maxthrust = throttle
            print(speed, throttle, sep="\t")

            # throttle *= 20

            pulsewidth = 1500 + (500 * max(min(throttle, 1), -1))
            # print(output)
            pi.set_servo_pulsewidth(self.pin, pulsewidth)


    def set_pw(self, pulsewidth):
        pi.set_servo_pulsewidth(self.pin, pulsewidth)

        # self
        # self.pwm.ChangeDutyCycle()

    def get_moment_coefficients(self):
        p = radians(90-self.phi)
        t = radians(90+self.theta)
        x = self.x
        y = self.y
        z = self.z

        sinp = sin(p)
        sint = sin(t)
        cost = cos(t)
        cosp = cos(p)

        return [
            (z*sinp*sint) - (y*cosp),
            (x*cosp) - (z*sinp*cost),
            (y*sinp*cost) - (x*sinp*sint)
        ]

    def get_speed_bounds(self):
        return self.speedbound_reverse, self.speedbound_forward

    def serialize(self):
        return {
            "force_coefficients": self.get_force_coefficients(),
            "moment_coefficients": self.get_moment_coefficients(),
            "speed": self.speed,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "phi": self.phi,
            "theta": self.theta,
            "speedbound_forward": self.speedbound_forward,
            "speedbound_reverse": self.speedbound_reverse,
        }


@functools.cache
def solve_motion(motors, Fx, Fy, Fz, Rx, Ry, Rz, optimize=True, limit=True):
    # print('@@@@@@@@@@@@@@@@@@@@@@')
    coefficients = []
    for motor in motors:
        coefficients.append(motor.get_force_coefficients() + motor.get_moment_coefficients())
        # print(motor, coefficients[-1])

    A = np.array(coefficients).transpose()
    b = np.array([Fx, Fy, Fz, Rx, Ry, Rz])


    bounds = ([i.speedbound_reverse for i in motors], [i.speedbound_forward for i in motors])

    solutions = lsq_linear(A, b, bounds=bounds).x

    # # print(b)
    # n = len(b)

    # # bounds = ([i.speedbound_reverse for i in motors], [i.speedbound_forward for i in motors]) if limit else (-np.inf, np.inf)
    # # solutions = lsq_linear(A, b, bounds=bounds, lsq_solver="exact", method="bvls").x
    # # print(solutions)

    # # time_a = time.time()
    # solutions = np.linalg.lstsq(A, b, rcond=None)[0]
    # if optimize:
    #     def fun(x):
    #         s = sum(np.abs(np.dot(A,x)-b))
    #         print(s)
    #         return s
    #     time_b = time.time()
    #     try:
    #         sol = minimize(fun, solutions, method='L-BFGS-B', bounds=[(i.get_speed_bounds() if limit else (None, None)) for i in motors])
    #     except ValueError as e:
    #         print(e)
    #         raise e
    #         sol = {"x":[0,0,0,0,0,0]}
    #     # print(time.time()-time_b, time_b- time_a)
    #     solutions = sol['x']

# #     print('================')
# #     if limit:
# #         for speed in solutions:
# #             print(speed)
# #     print('================')

    rA = solutions * A

    return {"speeds": list(solutions), "actual": list(map(sum, rA))}



def get_movement(motors):
    coefficients = []

    for motor in motors:
        coefficients.append(motor.get_force_coefficients() + motor.get_moment_coefficients())

    A = np.array(coefficients).transpose()

    speeds = np.array(list(map(lambda i:i.speed, motors)))

    rA = speeds * A

    # print(rA)

    return list(map(sum, rA))


# print(get_movement(motors))
# solve(motors, 1,0,0,0,0,0)
# solve(motors, 0,1,0,0,0,0)
# solve(motors, 0,0,1,0,0,0)
# solve(motors, 0,0,0,1,0,0)
# solve(motors, 0,0,0,0,1,0)
# solve(motors, 0,0,0,0,0,1)
# solve(motors, 0,0,0,0,0,0)
