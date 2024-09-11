import simulation

class LEDS():
    n_leds = 0
    buffer = list()

    def __init__(self, n):
        self.n_leds = n
        self.buffer = [(0,0,0,1)] * n

    def set_led(self, index, r, g, b, a=1):
        self.buffer[index] = (r, g, b, a)
        if simulation.is_simulated():
            simulation.set_leds(self.buffer)


    def set_leds(self, r, g, b, a=1):
        for i in range(self.n_leds):
            self.set_led(i, r, g, b, a)
