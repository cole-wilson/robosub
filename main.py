import sys
import time
import logger
import mainloop
import communication
import threading

def main(_):
    comthread = threading.Thread(target=communication.listen, args=['', 20001], daemon=True)
    comthread.start()

    print('mainloop has started...')
    mainloop.setup()
    while True:
        if comthread.is_alive():
            mainloop.loop()
        else:
            break

if __name__ == "__main__":
    try:
        main(sys.argv)
    except (Exception, KeyboardInterrupt) as e:
        print('...mainloop has ended')
        logger.add(time.time(), repr(e))
        logger.save()
        raise e
