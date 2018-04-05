from sensing.takePicture.camera_sensor import CameraSensor
import time


cam_sense = CameraSensor()

cam_sense.start()
while True:
  print cam_sense.get_camera_events(3)
  time.sleep(.5)
