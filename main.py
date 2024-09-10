import sys
import mainloop
import simulation
import communication
import threading
import time

def main(_):
    comthread = threading.Thread(target=communication.listen, args=['', 20001], daemon=True)
    comthread.start()

    if simulation.is_simulated():
        simthread = threading.Thread(target=simulation.main, daemon=True)
        simthread.start()

    print('mainloop has started...')
    mainloop.setup()
    while True:
        if comthread.is_alive():

            if communication.network["enabled"]:
                mainloop.loop()
            else:
                mainloop.disabled()
            time.sleep(0.001)
        else:
            break

if __name__ == "__main__":
    try:
        main(sys.argv)
    except (Exception, KeyboardInterrupt) as e:
        print('...mainloop has ended', e)
        raise e
