import simulation
import time


if not simulation.is_simulated():
    import board
    import neopixel



class LEDS():
    n_leds = 0
    buffer = list()

    def __init__(self, pin, n):
        self.n_leds = n
        self.buffer = [(0,0,0,1)] * n
        if not simulation.is_simulated():
            # pind = board.D18
            #IMPLEMENT!
            self.pixels = neopixel.NeoPixel(board.D18, n)
            # self.strip.clear_strip()


    def set_led(self, index, r, g, b, a=1, show=True):
        self.buffer[index] = (r, g, b, a)

        if simulation.is_simulated():
            simulation.set_leds(self.buffer)
        else:
            self.pixels[index] = (r, g, b)

    def set_leds(self, r, g, b, a=1):
        for i in range(self.n_leds):
            self.buffer[i] = (r, g, b, a)
        if not simulation.is_simulated():
            self.pixels.fill((r,g,b))

        if simulation.is_simulated():
            simulation.set_leds(self.buffer)

    def clear(self):
        self.buffer = [(0,0,0,1)] * self.n_leds
        if simulation.is_simulated():
            simulation.set_leds(self.buffer)

        if not simulation.is_simulated():
            self.pixels.fill((0,0,0))
