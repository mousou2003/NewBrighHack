import platform
import PS3Controller
import Logger
import CarControllerInterface
import CarControllers
import QRCodeDetector
import CameraController
import cv2
import numpy as np

qrcodefile = "qrcode-learnopencv"
goleft = "Goleft"
goright = "Goright"
gostraight = "Gostraight"
stop = "stop"

class PlatformController:
    def __init__(self, loglevel = Logger.LogLevel.NONE):
        self._logger = Logger.Logger(loglevel)
        runningPlatform =platform.platform()
        self.isRaspberryPI = False
        self.controller_increment = 32767/10
        self.run = True
        self._logger.log("Running on: "+runningPlatform)
        if runningPlatform.find("Linux")>-1: 
            self.displayAvailable = PlatformController.X_is_running()
            self.joystickController = PS3Controller.PS3Controller(interface="/dev/input/js0", loglevel=Logger.LogLevel.DISPLAY, callback=self)
            self.carController = CarControllers.OsoyooCarController(loglevel=loglevel)
            self.isRaspberryPI = True # we assume Linux is RaspberryPi
        elif runningPlatform.find("Windows")>-1:   
            self.displayAvailable = True #we assume we always have display available in Windows
            self.joystickController = PS3Controller.PS3Controller(interface="/dev/input/js0", loglevel=Logger.LogLevel.DISPLAY)
            self.carController = CarControllerInterface.CarControllerMoke(loglevel=loglevel)
        else:
            raise Exception("Platform {} not Supported"%runningPlatform)
        self._lefMotorThrottle = 0
        self._RightMotorThrottle = 0
        #self._camera = CameraController.CameraController(loglevel=self._logger)
        #self._qrCodeDetector = QRCodeDetector.QRCodeDetector(self.isRaspberryPI, self._logger)

    def stop(self):
        self.carController.Stop()
        self.joystickController.stopThead()
        self._camera.stop()
    
    def NormalizeSteps(self, value):
        return -int(10*value/self.controller_increment)

    def Left_up(self, value):
        self._lefMotorThrottle = self.NormalizeSteps(value)

    def Left_down(self, value):
        self._lefMotorThrottle = self.NormalizeSteps(value)

    def Left_at_rest(self):
         self._lefMotorThrottle = 0

    def Right_up(self, value):
        self._RightMotorThrottle = self.NormalizeSteps(value)
    
    def Right_down(self, value):
        self._RightMotorThrottle = self.NormalizeSteps(value)
        
    def Right_at_rest(self):
         self._RightMotorThrottle = 0

    def on_Start_pressed(self):
        self._logger.log("PlatformController:on_Start_pressed")
        self.run = False

    def isRunning(self):
        return self.run

    def isBatteryLevelSafe(self):
        return self.carController.ReadBatteryLevel() > 0
    
    def UpdateMotors(self):
        self._logger.log("PlatformController:UpdateMotors")
        self.carController.LefMotorControl(self._lefMotorThrottle)
        self.carController.RightMotorControl(self._RightMotorThrottle)

    def Connect(self):
        self._logger.log("PS3 Controller Connected")

    def Disconnect(self):
        self._logger.log("PS3 Controller Disconnected")

    def X_is_running():
        from subprocess import Popen, PIPE
        p = Popen(["xset", "-q"], stdout=PIPE, stderr=PIPE)
        p.communicate()
        return p.returncode == 0

    def DriveOnQR(self):
        self._logger.log("PlatformController:DriveOnQR")
        while (self._camera.last_frame is None):
            continue
        copy = self._camera.last_frame.copy()
        data,x,y,w,h = self._qrCodeDetector.Decode(copy)
        cv2.rectangle(copy,(x,y),(x+w,y+h),(255,0,0),5)
        if len(data)>0:
            cv2.putText(copy,"Decoded Data : {}".format(data), (10, 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            self._logger.log("Decoded Data : {}".format(data))
        else:  
            cv2.putText(copy,"QR Code not detected", (10, 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 255), 1)
            self._logger.log("QR Code not detected")
        cv2.imshow('frame', copy)

        if (data.find(goleft)>-1):
            self._logger.log("->Going left")
            self._RightMotorThrottle = 100
            self._lefMotorThrottle = -50
        elif (data.find(goright)>-1):
            self._logger.log("->Going rigth")
            self._RightMotorThrottle = -50
            self._lefMotorThrottle = 100
        elif (data.find(gostraight)>-1):
            self._logger.log("->Going straight")
            self._RightMotorThrottle = int( 50+ 50 * 1 if (self._camera.width/2 - (w/2 + x))/self._camera.width/2>0 else 0)
            self._lefMotorThrottle = int(50* 1 if (self._camera.width/2 + (w/2 + x))/self._camera.width/2 else 0)
        # else:
        #     self._logger.log("->stop")
        #     #self._RightMotorThrottle = 0
        #     #self._lefMotorThrottle = 0
