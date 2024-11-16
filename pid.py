from simple_pid import PID as _PID
import math

class PID():
    _pid = None
    rollover = math.pi * 2

    def __init__(self, *args, rollover_at=2*math.pi, **kwargs):
        self.rollover = rollover_at
        self._pid = _PID(*args, **kwargs)

    def calculate(self, state):
        return self._pid(state)
        setpoint = self._pid.setpoint
        if abs(setpoint - state) > abs(setpoint - (state - self.rollover)):
            return self._pid(state - self.rollover)
        else:
            return self._pid(state)

    def set(self, setpoint):
        self._pid.setpoint = setpoint
