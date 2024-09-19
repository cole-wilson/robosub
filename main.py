import sys
import mainloop
import simulation
import communication
import threading
import time
import os
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

    simulation.ge_ds_thread().start()
    if simulation.is_simulated():
        webbrowser.open("http://localhost:8080")

    print('mainloop has started...')
    communication.network.Simulated = simulation.is_simulated()
    mainloop.setup()

    # last = time.time()

    while True:
        if comthread.is_alive():
            at = time.time()
            communication.network.heartbeat = time.time()
            # print(communication.network.enabled, end="\r")
            if time.time() - at > 0.02:
                print("@@@@@@@@@@@@", at)
            if communication.network["enabled"]:
                mainloop.loop()
            else:
                mainloop.disabled()
            time.sleep(0.001)
        else:
            break

if __name__ == "__main__":
    try:
        if not simulation.is_simulated():
            os.chdir("/home/robosub/code/")
        # with contextlib.redirect_stdout(TeeIO(sys.stdout)):
        main(sys.argv)
    except (Exception, KeyboardInterrupt) as e:
        print('...mainloop has ended', e)
        raise e
