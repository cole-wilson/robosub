import simulation

if not simulation.is_simulated():
    import pigpio
    pi = pigpio.pi()


class DigitalInput():
    pin = 0
    default = 0

    def __init__(self, pinBCM, default=0):
        if pinBCM and not simulation.is_simulated():
            self.pin = pinBCM
            self.default = default
            # pi.set_servo_pulsewidth(self.pin, 1500)
            # time.sleep(0.3)

    def get_value(self):
        if not simulation.is_simulated():
            return pi.read(self.pin)
        else:
            return self.default
