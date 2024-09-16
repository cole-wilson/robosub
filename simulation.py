import socket
from communication import network
import http.server
import socketserver
import webbrowser
import os


def is_simulated():
    return socket.gethostname() != "dirty-bubble"

def expose_motors(*m):
    network["Sim/Motors"] = list(map(lambda i: i.serialize(), m))

def set_movement(m):
    network["Movement"] = m

def get_sim_camera():
    try:
        data = network["Sim/Camera"]
        return data
    except AttributeError:
        return None

def set_leds(buffer):
    try:
        network["Sim/LEDs"] = buffer
        return True
    except AttributeError:
        return False

def main():
    PORT = 8080

    os.chdir("ds")
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *i: 1

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.allow_reuse_address = True
        print("serving ds...", PORT)
        if is_simulated():
            webbrowser.open("http://localhost:8080/sim.html")
        httpd.serve_forever()
