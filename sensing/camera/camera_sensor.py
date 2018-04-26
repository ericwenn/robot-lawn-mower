#import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty
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
    while True:
      image = self.cam_stream.get_latest_image()
      if not image == None:
        analyzed, intermediates, _ = analyze_image(image)
        # store_image(image, 'in', 1 + len(intermediates))
        # for intermediate in intermediates:
        #   store_image(intermediate[1], intermediate[0], 1 + len(intermediates))
          
        time.sleep(0.01)
        self.send(analyzed)
class CameraSensor(object):
    def __init__(self):
        self.thread = CameraSensorThread()

    def start(self):
        self.thread.daemon = True
        self.thread.start()



def start():
  cam_sense = CameraSensor()
  cam_sense.start()
  camera_vis = CameraVisualizer()
  camera_vis.start()



if __name__ == "__main__":
  start()
  while True:
    time.sleep(5)