import simulation
import time

if not simulation.is_simulated():
    import ledshim
    ledshim.set_clear_on_exit()


class LEDS():
    n_leds = 0
    buffer = list()

    def __init__(self, n):
        self.n_leds = n
        self.buffer = [(0,0,0,1)] * n
        if not simulation.is_simulated():
            ledshim.clear()

    def set_led(self, index, r, g, b, a=1, show=True):
        # print(9876543456789)
        self.buffer[index] = (r, g, b, a)
        if simulation.is_simulated():
            simulation.set_leds(self.buffer)
        else:
            ledshim.set_pixel(index, r, g, b, a)
            if show:
                ledshim.show()

    def set_leds(self, r, g, b, a=1):
        for i in range(self.n_leds):
            self.buffer[i] = (r, g, b, a)
        if not simulation.is_simulated():
            ledshim.set_all(r, g, b, a)
            ledshim.show()
            # print('leds',time.time()-at)

    def clear(self):
        self.buffer = [(0,0,0,1)] * self.n_leds
        if not simulation.is_simulated():
            ledshim.clear()
