from pyPS4Controller.controller import Controller


class PS4Controller(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        #self.listen(on_connect=self.connect, on_disconnect=self.disconnect)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")

    def connect(self):
        # any code you want to run during initial connection with the controller
        pass

    def disconnect(self):
        # any code you want to run during loss of connection with the controller or keyboard interrupt
        pass