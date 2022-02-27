import threading
import time
import cv2
import numpy as np
import Logger

# Define the thread that will continuously pull frames from the camera
class CameraController(threading.Thread):
    def __init__(self, name='camera-buffer-cleaner-thread', loglevel = Logger.LogLevel.NONE):
        self.width = 1280
        self.height = 1024
        self._logger = Logger.Logger(loglevel)
        self._logger.log("Init CameraController")
        self.last_frame = None
        self._video = cv2.VideoCapture(0)
        self._video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        super(CameraController, self).__init__(name=name)
        self._stop_event = threading.Event()
        self.start()
    
    def __del__(self):
        self._logger.log("Stopping CameraController")

    def run(self):
        while True:
            ret, self.last_frame = self._video.read()
            self.lastFrameTime = time.time()
            if self.stopped():
                break
    def stop(self):
        self._stop_event.set()
        self.join()
        self._video.release()
                
    def stopped(self):
        return self._stop_event.is_set()
