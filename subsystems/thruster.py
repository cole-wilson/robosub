import numpy as np
from math import sin, cos, tan, radians
from scipy.optimize import minimize



np.set_printoptions(precision=3, suppress=True)


class Thruster():
    def __init__(self, x, y, z, theta, phi, pin=None):
        self.x = x
        self.y = y
        self.z = z
        self.phi = phi
        self.theta = theta

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



motors = [
    Thruster(-1,2,0, -135, 0),
    Thruster(1,2,0, 135, 0),
    Thruster(1,-2,0, 45, 0),
    Thruster(-1,-2,0, -45, 0),
    Thruster(-1,0,0, 0, 90),
    Thruster(1,0,0, 0, 90),
]

# print(np_cf)
# print(np_cf_t)

def solve(motors, Fx, Fy, Fz, Rx, Ry, Rz):
    coefficients = []
    for motor in motors:
        coefficients.append(motor.get_force_coefficients() + motor.get_moment_coefficients())

    A = np.array(coefficients).transpose()
    b = np.array([Fx, Fy, Fz, Rx, Ry, Rz])
    n = len(b)

    # print(np_coefficients)
    # print(np_answers)

    # np_radii = np.linalg.lstsq(A, b, rcond=None)[0]
    fun = lambda x: np.linalg.norm(np.dot(A,x)-b)
    sol = minimize(fun, np.zeros(n), method='L-BFGS-B', bounds=[(-0.75,1) for _ in range(n)])
    np_radii = sol['x']

    # print(np_radii)

    # print(np_radii)

    # print(list(map(sum, list(np_radii * np_coefficients))))
    print(b)

    print("x_n =", list(map(lambda i:i.x, motors)))
    print("y_n =", list(map(lambda i:i.y, motors)))
    print("z_n =", list(map(lambda i:i.z, motors)))
    print("p_n =", list(map(lambda i:90-i.phi, motors)))
    print("t_n =", list(map(lambda i:90+i.theta, motors)))
    print("r_n =", list(map(lambda i: round(i,2), np_radii)))
    print()
    return np_radii

solve(motors, 1,0,0,0,0,0)
solve(motors, 0,1,0,0,0,0)
solve(motors, 0,0,1,0,0,0)
solve(motors, 0,0,0,1,0,0)
solve(motors, 0,0,0,0,1,0)
solve(motors, 0,0,0,0,0,1)
# solve(motors, 0,0,0,0,0,0)
