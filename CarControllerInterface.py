import Logger

class CarControllerInterface :
    def Move(angle, speed):
        pass
    def Stop():
        pass
    def Rotate(direction, speed):
        pass
    def CheckWheels():
        pass

class CarControllerMoke :
    def __init__(self, loglevel = Logger.LogLevel.NONE):
        self._logger = Logger.Logger(loglevel)
        self._logger.log("CarControllerMoke:Init")

    def Move(self, angle, speed):
        self._logger.log("CarControllerMoke:Move")
        pass

    def Stop(self):
        self._logger.log("CarControllerMoke:Stop")
        pass

    def Rotate(self, direction, speed):
        self._logger.log("CarControllerMoke:Rotate")
        pass

    def CheckWheels(self):
        self._logger.log("CarControllerMoke:CheckWheels")
