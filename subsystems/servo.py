import simulation

if not simulation.is_simulated():
    import pigpio
    pi = pigpio.pi()


class Servo():
    angle = 0
    pin = 0

    def __init__(self, pinBCM):
        if pinBCM and not simulation.is_simulated():
            self.pin = pinBCM
            # pi.set_servo_pulsewidth(self.pin, 1500)
            # time.sleep(0.3)

    def set_angle(self, angle):
        self.angle = angle
        if not simulation.is_simulated():
            pw = 1500 # * angle # or something
            pi.set_servo_pulsewidth(self.pin, pw)
