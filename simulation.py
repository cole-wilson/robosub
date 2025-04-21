import socket
from communication import network
from http import server
# import http.server
import socketserver
import webbrowser
import os
import io
from threading import Thread, Condition

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



if not is_simulated():
    import picamera2
    from picamera2.encoders import JpegEncoder
    from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                print("camera stream error",e)
        else:
            return super().do_GET()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

output = StreamingOutput()

def serve():
    global output
    os.chdir('ds')

    address = ('', 8000)

    serverc = StreamingServer
    serverc.allow_reuse_address = True
    serverc.allow_reuse_port = True
    server = serverc(address, StreamingHandler)

    print('serving ds on', address)
    if is_simulated():
        output = None
        server.serve_forever()
    else:
        ...
        # camera = picamera2.Picamera2()
        # camera.configure(camera.create_video_configuration(main={"size": (270, 180)}))
        # with camera:
        #     # output = StreamingOutput()
        #     # camera.start_recording(output, format='mjpeg')
        #     camera.start_recording(JpegEncoder(), FileOutput(output))
        #     try:
        server.serve_forever()
        #     finally:
        #         camera.stop_recording()

def ge_ds_thread():
    # PORT = 8080

    # os.chdir("ds")
    # handler = http.server.SimpleHTTPRequestHandler
    # handler.log_message = lambda *_:True

    # server = socketserver.TCPServer



    # httpd = server(("", PORT), handler)
    # httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # print("serving DS server on port", PORT)
    # return Thread(target=httpd.serve_forever, daemon=True)
    return Thread(target=serve, daemon=True)
