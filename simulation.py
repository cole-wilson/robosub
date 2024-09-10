import eel
import socket
from communication import network

motors = []
movement = [0,0,0, 0,0,0]

def is_simulated():
    return socket.gethostname() != "dirty-bubble"

def expose_motors(*m):
    global motors
    motors = m

@eel.expose
def get_motors():
    return list(map(lambda i: i.serialize(), motors))

@eel.expose
def set_network(key, value):
    network[key] = value

@eel.expose
def get_movement():
    return movement

def set_movement(m):
    global movement
    movement = m

def get_sim_camera():
    try:
        data = eel.getcanvasdata()();
        return data
    except AttributeError:
        return None

def main():
    print('started eel websim')
    eel.init('websim')
    eel.start('index.html', mode='default')
