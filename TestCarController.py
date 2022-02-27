from CarControllers import OsoyooCarController
import Logger
import time

print ("Doing basic wheel check")
controller = OsoyooCarController(loglevel=Logger.LogLevel.DISPLAY)
#controller.CheckWheels()
while True:
    print(controller.ReadBatteryLevel())
    time.sleep(2)