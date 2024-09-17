import sys
import mainloop
import simulation
import communication
import threading
import time
import webbrowser
import contextlib

class TeeIO:
    def __init__(self, original):
        self.original = original

    def write(self, value):
        self.original.write(value)
        self.original.flush()
        communication.stdoutQueue.put(value)

def main(_):
    comthread = threading.Thread(target=communication.listen, args=['', 20001], daemon=True)
    comthread.start()

    # if simulation.is_simulated():
    simulation.ge_ds_thread().start()
    webbrowser.open("http://localhost:8080")

    print('mainloop has started...')
    mainloop.setup()
    while True:
        if comthread.is_alive():
            communication.network.heartbeat = time.time()
            # print(communication.network, end="\n\n")
            if communication.network["enabled"]:
                mainloop.loop()
            else:
                mainloop.disabled()
            time.sleep(0.001)
        else:
            break

if __name__ == "__main__":
    try:
        with contextlib.redirect_stdout(TeeIO(sys.stdout)):
            main(sys.argv)
    except (Exception, KeyboardInterrupt) as e:
        print('...mainloop has ended', e)
        raise e
