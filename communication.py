import json
import websockets.sync.server
import websockets.exceptions
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
        # input((name, value))
        old = None
        if name in self.__data:
            old = self.__data[name]

        self.__data[name] = value

        if not from_remote:# and old != value:
            tosendlock.acquire()
            tosend["values"][name] = value
            tosendlock.release()

    def __setitem__(self, name, value, from_remote=False):
        return self.__setattr__(name, value, from_remote)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __repr__(self):
        return repr(self.__data)

    def getdata(self):
        return self.__data

network = NetworkData()



def handler(conn):
    try:
        conn.send(json.dumps(network.getdata()))
        while True:
            # fetch any new data from the driverstation
            try:
                # print('fetching remote')
                data = conn.recv(timeout=0.05)
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
            conn.send(json.dumps(tosend["values"]))
            tosend["values"] = {}
            tosendlock.release()
    except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
        network.enabled = False
        print('client ended connection')

def listen(host, port):
    global network

    with websockets.sync.server.serve(handler, host=host, port=port) as server:
        server.serve_forever()
