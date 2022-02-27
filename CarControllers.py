import CarControllerInterface
import time
import Logger
import RPi.GPIO as GPIO

class OsoyooCarController():

    def __init__(self, loglevel = Logger.LogLevel.NONE):
        self._logger = Logger.Logger(loglevel)
        self._logger.log("Init motors and GPIO")
        # self._goRightPinout= (GPIO.HIGH,GPIO.LOW,GPIO.HIGH,GPIO.LOW)
        # self._goLeftPinout = (GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.HIGH)
        # self._goForwardPinout = (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH)
        # self._goBackwardPinout = (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW)
        self._goBackwardPinout= (GPIO.HIGH,GPIO.LOW,GPIO.HIGH,GPIO.LOW)
        self._goForwardPinout = (GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.HIGH)
        self._goLeftPinout = (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH)
        self._goRightPinout = (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW)
        self._leftMotorsForwardPinout = (GPIO.LOW,GPIO.HIGH)
        self._rightMotorsForwardPinout = (GPIO.LOW,GPIO.HIGH)
        self._leftMotorsBackwardPinout = (GPIO.HIGH,GPIO.LOW)
        self._rightMotorsBackwardPinout = (GPIO.HIGH,GPIO.LOW)
        self._leftMotors_channel = (11,18)
        self._rightMotors_channel = (15,16) 
        self._motor_channel = (11,18,15,16)
        self._board_channel = (11,18,15,16,12,13)
        self._battery_readingPin = 37
        self._max_duty_cycle = 100
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._battery_readingPin, GPIO.IN)
        GPIO.setup(self._board_channel, GPIO.OUT)
        self._leftMotors=GPIO.PWM(12,1000)
        self._rightMotors=GPIO.PWM(13,1000)
        self._leftMotors_dutyCycle = 0
        self._rightMotors_dutyCycle = 0
        self._leftMotors.start(0)
        self._rightMotors.start(0)

    def __del__(self):
        self._logger.log("Stopping motors and cleaning up GPIO")
        self._leftMotors.stop()
        self._rightMotors.stop()
        GPIO.cleanup()

    def Change_dutycycle(self, left, right):
        self._logger.log("OsoyooCarController:Change_dutycycle")
        left_gradiant = -1 if self._leftMotors_dutyCycle>left else 1
        right_gradiant = -1 if self._rightMotors_dutyCycle>right else 1
        for dc in range(self._leftMotors_dutyCycle, left, left_gradiant):
            self._leftMotors.ChangeDutyCycle(dc)
            self._leftMotors_dutyCycle = dc
            time.sleep(0.005)
        for dc in range(self._rightMotors_dutyCycle, right, right_gradiant):
            self._rightMotors.ChangeDutyCycle(dc)
            self._rightMotors_dutyCycle = dc
            time.sleep(0.005)
    
    def Move(self, angle, speed):
        self._logger.log("OsoyooCarController:Move")
        assert angle <= 90 and angle >= -90 , "angle needs to be between -90 and 90"
        if angle > 0:
            tagetLeft_duty_cycle = self._max_duty_cycle * angle/90
            tagetRight_duty_cycle = self._max_duty_cycle * (1-angle/90)
        elif angle < 0:
            tagetLeft_duty_cycle = self._max_duty_cycle * (1-angle/90)
            tagetRight_duty_cycle = self._max_duty_cycle * angle/90
        else:
            tagetLeft_duty_cycle = self._max_duty_cycle
            tagetRight_duty_cycle = self._max_duty_cycle      
        left = tagetLeft_duty_cycle*speed
        right = tagetRight_duty_cycle*speed
        self.Change_dutycycle(left, right, 1)

    def Stop(self):
        self._logger.log("OsoyooCarController:Stop")
        self.Change_dutycycle(0,0)

    def Rotate(self, direction, speed):
        self._logger.log("OsoyooCarController:Rotate")
        pass

    def Forward(self, value):
        GPIO.output(self._motor_channel, self._goForwardPinout) 
        self.Change_dutycycle(left=value,right=value)

    def Backward(self, value):
        GPIO.output(self._motor_channel, self._goBackwardPinout) 
        self.Change_dutycycle(left=value,right=value)
    
    def Rigth(self, value):
        GPIO.output(self._motor_channel, self._goRightPinout)
        self.Change_dutycycle(left=value,right=value)
    
    def Left(self, value):
        GPIO.output(self._motor_channel, self._goLeftPinout)
        self.Change_dutycycle(left=value,right=value)

    def MotorControl(self, targetSpeed, ductyCycleController, currentSpeed, channel, BackwardPinout, ForwardPinout):
        self._logger.log("OsoyooCarController:MotorControl current %d target %d"%(currentSpeed, targetSpeed))
        assert targetSpeed <= 100 and targetSpeed >= -100 , "angle needs to be between -90 and 90"

        gradiant = -1 if currentSpeed>targetSpeed else 1       
        for dc in range(currentSpeed, targetSpeed+gradiant, gradiant):
            ductyCycleController.ChangeDutyCycle(abs(dc))
            currentSpeed = dc
            if currentSpeed > 0 :
                GPIO.output(channel, ForwardPinout)
            else:
                GPIO.output(channel, BackwardPinout)
            time.sleep(0.001)
 
        return currentSpeed

    def LefMotorControl(self, value):
        self._logger.log("OsoyooCarController:LefMotorControl value %d"%value)
        if value == self._leftMotors_dutyCycle:
            self._logger.log("OsoyooCarController:LefMotorControl same value no action")
            return
        self._leftMotors_dutyCycle = self.MotorControl(value, self._leftMotors, self._leftMotors_dutyCycle,self._leftMotors_channel, \
            self._leftMotorsForwardPinout, self._leftMotorsBackwardPinout)
        return
 
    def RightMotorControl(self, value):
        self._logger.log("OsoyooCarController:RightMotosControl value %d"%value)
        if value == self._rightMotors_dutyCycle:
            self._logger.log("OsoyooCarController:LefMotorControl same value no action")
            return
        self._rightMotors_dutyCycle = self.MotorControl(value, self._rightMotors, self._rightMotors_dutyCycle,self._rightMotors_channel, \
            self._rightMotorsForwardPinout, self._rightMotorsBackwardPinout)
        return
        
    def CheckWheels(self):
        self._logger.log("OsoyooCarController:CheckWheels")
        self.Left(50)
        time.sleep(5)
        self.Rigth(50)
        time.sleep(5)
        self.Forward(50) 
        time.sleep(5)
        self.Backward(50)
        time.sleep(5)
        self.Stop()

    def ReadBatteryLevel(self):
        return GPIO.input(self._battery_readingPin)
