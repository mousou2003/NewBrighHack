# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 11:22:07 2021

@author: mouso
"""
from OsyooCarController import OsoyooCarController
import cv2
import numpy as np
import sys
import time
import qrcode
import PS3Controller
import threading

qrcodefile = "qrcode-learnopencv"
goleft = "Goleft"
goright = "Goright"
gostraight = "Gostraight"
stop = "stop"
qrDecoder = cv2.QRCodeDetector()

# Define the thread that will continuously pull frames from the camera
class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self._stop_event = threading.Event()
        self.start()

    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()
            self.lastFrameTime = time.time()
            if self.stopped():
                break
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()
            
def X_is_running():
    from subprocess import Popen, PIPE
    p = Popen(["xset", "-q"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    return p.returncode == 0

def MakeQRCode():
    code = qrcode.make('Bonjour Evie!')
    code.save(qrcodefile+".png")
    code = qrcode.make(goleft)
    code.save(goleft+".png")
    code = qrcode.make(goright)
    code.save(goright+".png")
    code = qrcode.make(gostraight)
    code.save(gostraight+".png")
    
    if len(sys.argv)>1:
        inputImage = cv2.imread(sys.argv[1])
    else:
        inputImage = cv2.imread(qrcodefile+".png")
    
    
     # Detect and decode the qrcode
    data,bbox,rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if len(data)>0:
        print("Decoded Data : {}".format(data))
        rectifiedImage = np.uint8(rectifiedImage)
        cv2.imshow("Rectified QRCode", rectifiedImage)
    else:
        print("QR Code not detected")
    cv2.imshow("Results", inputImage)
            
# define a video capture object

try:
    #MakeQRCode()
    import platform
    isRaspberryPI = False
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam_cleaner = CameraBufferCleanerThread(vid)
    print (platform.platform())
    if platform.platform().find("Linux")>-1: 
        import OsyooCarController
        carconrtoller = OsoyooCarController()
        from pyzbar import pyzbar
        displayAvailable = X_is_running()
        isRaspberryPI = True
        controller = PS3Controller.PS3Controller(interface="/dev/input/js0")
    else:
        #we assume we always have display available in Windows
        displayAvailable = True
    

    print("Starting loop")
    current_state = stop
    while(True):
          
        # Capture the video frame
        # by frame

        while (cam_cleaner.last_frame is None):
            continue

        frame = cam_cleaner.last_frame
        copy = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.threshold(frame,200,255,cv2.THRESH_BINARY)[1]
        points = cv2.findNonZero(frame)
        x,y,w,h = cv2.boundingRect(points)
        print ("rectangle found {0},{1},{2},{3}".format(x,y,w,h))
        #frame = copy

        if w > 0 and h > 0 :
            analyze = copy[y:y+h, x:x+w]
        else:
            analyze = copy
        cv2.rectangle(copy,(x,y),(x+w,y+h),(255,0,0),5)

        # Display the resulting frame
        data =""
        if isRaspberryPI:
            for barcode in pyzbar.decode(analyze):
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                data = barcode.data.decode("utf-8")
        else:
            data,bbox,rectifiedImage = qrDecoder.detectAndDecode(analyze)
            x,y,w,h = cv2.boundingRect(bbox)
        cv2.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),5)
        if len(data)>0:
            cv2.putText(copy,"Decoded Data : {}".format(data), (10, 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            print("Decoded Data : {}".format(data))
        else:
            cv2.putText(copy,"QR Code not detected", (10, 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 255), 1)
            print("QR Code not detected")
    
        if displayAvailable:
            cv2.imshow('frame', copy)

        if isRaspberryPI:
            if (data.find(goleft)>-1):
               print("->Going left")
               if (current_state != goleft):
                   GPIO.output(motor_channel, goleftpinout)
                   ramp_up_dutycycle((ena,enb),max_duty_cycle)
                   current_state = goleft
            elif (data.find(goright)>-1):
               print("->Going rigth")
               if (current_state != goright):
                   GPIO.output(motor_channel, gorightpinout)
                   ramp_up_dutycycle((ena,enb),max_duty_cycle)
                   current_state = goright
            elif (data.find(gostraight)>-1):
               print("->Going straight")
               if (current_state != gostraight):
                   GPIO.output(motor_channel, gostraightpinout)
                   ramp_up_dutycycle((ena,enb),max_duty_cycle)
                   current_state = gostraight
            else:
               print("->stop")
               if (current_state != stop):
                   current_state = stop
                   ramp_down_dutycycle((ena,enb),max_duty_cycle)
          
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      

except cv2.error as err:
    print(err)
except KeyboardInterrupt:
    print ("Bye")
    # After the loop release the cap object
if isRaspberryPI:
    print("->stop")
    if ena is not None:
       ramp_down_dutycycle((ena,enb),max_duty_cycle)
    GPIO.cleanup()
    controller.stopThead()
    controller.join()
cam_cleaner.stop()
cam_cleaner.join()
vid.release()    
cv2.destroyAllWindows()
sys.exit()
