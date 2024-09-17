import socket
from communication import network
import http.server
import socketserver
import webbrowser
import os
from threading import Thread

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

def ge_ds_thread():
    PORT = 8080

    os.chdir("ds")
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *i: 1

    server = socketserver.TCPServer

    server.allow_reuse_address = True
    server.allow_reuse_port = True

    httpd = server(("", PORT), handler)
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("serving DS server on port", PORT)
    return Thread(target=httpd.serve_forever, daemon=True)
