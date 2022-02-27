import CameraController
import cv2
import numpy as np
import QRCodeDetector
import Logger
import sys

logger = Logger.Logger(Logger.LogLevel.DISPLAY)

camera = CameraController.CameraController(loglevel=logger)
qrCodeDetector = QRCodeDetector.QRCodeDetector(isRaspberryPI=False, loglevel=logger)

while(True):
 
    while (camera.last_frame is None):
        continue

    copy = camera.last_frame.copy()
    data,x,y,w,h = qrCodeDetector.Decode(copy)
    cv2.rectangle(copy,(x,y),(x+w,y+h),(255,0,0),5)
    if len(data)>0:
        cv2.putText(copy,"Decoded Data : {}".format(data), (10, 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        logger.log("Decoded Data : {}".format(data))
    else:  
        cv2.putText(copy,"QR Code not detected", (10, 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 255), 1)
        logger.log("QR Code not detected")
    cv2.imshow('frame', copy)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.stop()
cv2.destroyAllWindows()
sys.exit()