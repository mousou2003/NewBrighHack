import threading
import Logger
import cv2
import numpy as np
import qrcode
from pyzbar import pyzbar

class QRCodeDetector():
    def __init__(self, isRaspberryPI=False, loglevel = Logger.LogLevel.NONE):
        self._logger = Logger.Logger(loglevel)
        self._isRaspberryPI = isRaspberryPI
        if not self._isRaspberryPI:
            self._qrDecoder = cv2.QRCodeDetector()
    
    def Decode(self, frame):
        copy = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.threshold(frame,200,255,cv2.THRESH_BINARY)[1]
        points = cv2.findNonZero(frame)
        x,y,w,h = cv2.boundingRect(points)
        self._logger.log ("rectangle found {0},{1},{2},{3}".format(x,y,w,h))
        #frame = copy

        if w > 0 and h > 0 :
            analyze = copy[y:y+h, x:x+w]
        else:
            analyze = copy
        cv2.rectangle(copy,(x,y),(x+w,y+h),(255,0,0),5)

        # Display the resulting frame
        data =""
        if self._isRaspberryPI:
            for barcode in pyzbar.decode(analyze):
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                data = barcode.data.decode("utf-8")
        else:
            data,bbox,rectifiedImage = self._qrDecoder.detectAndDecode(analyze)
            x,y,w,h = cv2.boundingRect(bbox)
        
        return data,x,y,w,h
