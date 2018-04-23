#import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty
from picamera import PiCamera
from take_picture import take_picture
from analyze_image import analyze_image
import camera
import httplib
import json
from visualize_images import CameraVisualizer
from store_image import store_image
from camera_capture_stream import CameraCaptureStream

class CameraSensorThread(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.cam_stream = CameraCaptureStream()

  def send(self, reading):
    conn = httplib.HTTPConnection("cmg-navigating", "8080")
    body = json.dumps({ 'can_move': reading })
    try:
      conn.request("POST", "/camera", body, { 'Content-Type': 'application/json' })
      conn.getresponse()
    except:
      pass
        
  def run(self):
    self.cam_stream.start()
    i = 0
    while True:
      image = self.cam_stream.get_latest_image()
      if not image == None:
        analyzed, intermediates = analyze_image(image)
        store_image(image, 'in', 1)
        print "stored and analyzed image", i
        time.sleep(0.05)
        i += 1
#        self.send(analyzed)
class CameraSensor(object):
    def __init__(self):
        self.thread = CameraSensorThread()

    def start(self):
        self.thread.daemon = True
        self.thread.start()




if __name__ == "__main__":
    cam_sense = CameraSensor()
    cam_sense.start()
    camera_vis = CameraVisualizer()
    camera_vis.start()
    while True:
        time.sleep(5)