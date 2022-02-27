
from PlatformController import PlatformController
import Logger
import cv2
import numpy as np
import time
import sys

platformController = None

try:
    _logger = Logger.Logger(Logger.LogLevel.DISPLAY)
    platformController = PlatformController(Logger.LogLevel.DISPLAY)
    _logger.log("Starting loop")
    while((cv2.waitKey(1) & 0xFF != ord('q')) & platformController.isRunning() is True):
        #platformController.DriveOnQR()
        platformController.UpdateMotors()
        if platformController.isBatteryLevelSafe() is False:
            _logger.log("!!!!!!!!!!!!!!!!!! Battery is level Critical !!!!!!!!!!!!!!1")
        time.sleep(0.1)
    _logger.log("Stopping loop")

except cv2.error as err:
    print ("!!!!!!!!!! CV2 Exception trapped !!!!!!!!!!!!")
    print(err)
except Exception as err:
    print ("!!!!!!!!!! General Exception trapped !!!!!!!!!!!!")
    print(err)
except KeyboardInterrupt:
    print ("----------- Bye ---------------")
if platformController is not None:
    platformController.stop()
cv2.destroyAllWindows()
sys.exit()
