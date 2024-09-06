from subsystems.controller import Controller
from communication import network
import math
# import ledshim
# ledshim.set_clear_on_exit()


# spacing = 360.0 / 16.0
# hue = 0

controller = Controller()

def setup():
    ...
    # communication.network["r"] = 255
    # communication.network["g"] = 255
    # communication.network["b"] = 255

def r(a):
    return math.floor(100*a)/100
def loop():
    # print(network)
    # out = ""
    # for i in range(6):
        # out += f"Axis{i}: {r(controller.getAxis(i))}\t"
    print("axis0", controller.getAxis(0))
    ...
