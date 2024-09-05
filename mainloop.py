import communication

import ledshim
ledshim.set_clear_on_exit()


spacing = 360.0 / 16.0
hue = 0


def setup():
    communication.network["r"] = 255
    communication.network["g"] = 255
    communication.network["b"] = 255

def loop():
    # print(communication.network)
    # communication.network.b = input("b? > ")
    r = communication.network["r"]
    g = communication.network["g"]
    b = communication.network["b"]

    print(r, g, b)

    ledshim.set_all(r, g, b)
    ledshim.show()
