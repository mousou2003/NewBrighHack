import PS3Controller
import Logger

print ("test value %d"%10)
controller = PS3Controller.PS3Controller(interface="/dev/input/js0", loglevel=Logger.LogLevel.DISPLAY)
controller.stopThead()
controller.join()