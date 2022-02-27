from pyPS4Controller.controller import Controller
import threading
import Logger
 
class PS3Controller(threading.Thread, Controller):

    def __init__(self, interface="/dev/input/js0", loglevel = Logger.LogLevel.NONE, 
        connecting_using_ds4drv=False, name='PS3Controller-thread', callback =None):
        self._logger = Logger.Logger(loglevel)
        self._logger.log("Init PS3Controller")
        self._callback = callback
        threading.Thread.__init__(self, name=name)
        self._stop_event = threading.Event()
        Controller.__init__(self, interface=interface, connecting_using_ds4drv=connecting_using_ds4drv)
        self.start()

    def __del__(self):
        self.stopThead()

    def run(self):
        self._logger.log("PS3Controller thead started")
        self.listen(on_connect=self.connect, on_disconnect=self.disconnect)
        self._logger.log("PS3Controller thead stopping")
        self._stop_event.set()

    def stopThead(self):
        self.stop = True # stop the base class controller
        self._stop_event.set()
        self.join()
        
    def stopped(self):
        return self._stop_event.is_set()

    def on_L3_up(self, value):
        self._logger.log("PS3Controller:on_L3_up:%d " % value)
        self._callback.Left_up(value)

    def on_L3_down(self, value):
        self._logger.log("PS3Controller:on_L3_down:%d " % value)
        self._callback.Left_down(value)

    def on_L3_y_at_rest(self):
        self._logger.log("Mourad on_L3_y_at_rest")
        if self._callback is not None:
            self._callback.Left_at_rest()

    def on_R3_left(self, value):
        self._logger.log("PS3Controller:on_R3_up:%d " % value)
        if self._callback is not None:
            self._callback.Right_up(value)

    def on_R3_right(self, value):
        self._logger.log("PS3Controller:on_R3_down:%d " % value)
        if self._callback is not None:
            self._callback.Right_down(value)

    def on_R3_x_at_rest(self):
        self._logger.log("PS3Controller:on_R3_x_at_rest")
        if self._callback is not None:
            self._callback.Right_at_rest()
    
    def on_square_press(self):
        self._logger.log("PS3Controller:on_Start_pressed")
        self.stop = True # stop the base class controller
        self._stop_event.set()
        if self._callback is not None:
            self._callback.on_Start_pressed()

    def connect(self):
        self._logger.log("PS3Controller:connect")
        if self._callback is not None:
            self._callback.Connect()

    def disconnect(self):
        self._logger.log("PS3Controller:disconnect")
        if self._callback is not None:
            self._callback.Disconnect()


   