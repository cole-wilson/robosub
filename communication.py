import json
# import websockets.sync.server
import websockets.exceptions
import websockets.asyncio.server
import asyncio
from threading import Lock, Thread
from queue import Empty, Queue

tosend = {"values":{}}
tosendlock = Lock()

stdoutQueue = Queue()

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



async def handler(conn):
    print('new connection')
    try:
        await conn.send(json.dumps(network.getdata()))
        while True:
            # fetch any new data from the driverstation
            try:
                async with asyncio.timeout(0.05):
                    # print('fetching remote')
                    data = await conn.recv()
                    # print(data)
                    json_strings = data.replace('}{', '}|{').split('|')

                    try:
                        for k, v in json.loads(json_strings[-1]).items():
                            network.__setattr__(k, v, True)
                    except json.JSONDecodeError:
                        print(data)
                        pass
            except TimeoutError:
                pass

            # send any new data to the driverstation
            # print('sending from tosend')
            tosendlock.acquire()
            await conn.send(json.dumps(tosend["values"]))
            tosend["values"] = {}
            tosendlock.release()

            try:
                await conn.send(json.dumps({"__stdout":stdoutQueue.get(block=False)}))
            except Empty:
                pass

    except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK, ConnectionResetError) as e:
        # raise e
        network.enabled = False
        print('client ended connection')

def listen(host, port):
    async def main():
        async with websockets.asyncio.server.serve(handler, host, port):
            await asyncio.get_running_loop().create_future()  # run forever

    asyncio.run(main())
