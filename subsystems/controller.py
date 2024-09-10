from communication import network

class Controller():
    def getButton(self, id):
        value = network["Controller/Button"+str(id)] or 0
        # print(value)
        return bool(int(value))

    def getAxis(self, id):
        return network["Controller/Axis"+str(id)] or 0
