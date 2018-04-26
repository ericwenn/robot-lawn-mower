from GPS.booter import start as gps_start
from camera.camera_sensor import start as camera_start
from time import sleep
if __name__ == '__main__':
  gps_start()
  camera_start()
  while True:
    sleep(5)
