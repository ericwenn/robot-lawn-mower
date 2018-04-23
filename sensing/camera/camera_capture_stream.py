#import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty
from picamera import PiCamera
from take_picture import take_picture

class CameraCaptureStreamThread(Thread):
  def __init__(self, queue):
    self.queue = queue
    Thread.__init__(self)

  def run(self):
    with PiCamera(resolution = (144,96)) as c:
      while(True):
        img = take_picture(c)
        self.queue.put(img)



class CameraCaptureStream(object):
  def __init__(self):
    self.queue = Queue()
    self.latest_image = None
    self.thread = CameraCaptureStreamThread(self.queue)


  def start(self):
    self.thread.daemon = True
    self.thread.start()

  def get_latest_image(self):
    try:
      while True:
        self.latest_image = self.queue.get(block=False)
    except Empty:
      pass

    return self.latest_image
    




if __name__ == "__main__":
  cam_stream = CameraCaptureStream()
  cam_stream.start()
  while True:
    print cam_stream.get_latest_image()  
    time.sleep(.5)