import json
import socket
from threading import Lock

tosend = {"values":{}}
tosendlock = Lock()

class NetworkData():
    __data = {}

    def __getattr__(self, name):
        if name in self.__data:
            return self.__data[name]
        else:
            return None

    def __setattr__(self, name, value, from_remote=False):
        self.__data[name] = value

        if not from_remote:
            tosendlock.acquire()
            tosend["values"][name] = value
            tosendlock.release()

    def __setitem__(self, name, value, from_remote=False):
        return self.__setattr__(name, value, from_remote)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __repr__(self):
        return repr(self.__data)

network = NetworkData()

def listen(host, port):
    global network

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)

    while True:
        sock.settimeout(None)
        print('waiting for connection on', (host, port))
        conn, addr = sock.accept()
        conn.settimeout(0.05)

        with conn:
            print('connected by', addr)

            while True:
                # fetch any new data from the driverstation
                try:
                    # print('fetching remote')
                    data = conn.recv(1024).decode()
                    # print(data)
                    json_strings = data.replace('}{', '}|{').split('|')

                    try:
                        for k, v in json.loads(json_strings[-1]).items():
                            network.__setattr__(k, v, True)
                    except json.JSONDecodeError:
                        print(data)
                        pass
                except TimeoutError:
                    # print('pass fetch')
                    pass

                # send any new data to the driverstation
                # print('sending from tosend')
                tosendlock.acquire()
                conn.sendall(json.dumps(tosend["values"]).encode())
                tosend["values"] = {}
                tosendlock.release()
