from communication import network

class Controller():
    def getButton(self, id):
        value = network["Controller/Button"+str(id)] or 0
        # print(value)
        return value

    def getAxis(self, id):
        return network["Controller/Axis"+str(id)] or 0

    def setRumble(self, amount=1):
        network["Controller/Rumble"] = max(0, min(amount, 1))

    def stopRumble(self):
        return self.setRumble(0)
