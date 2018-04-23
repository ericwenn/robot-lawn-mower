#import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty
from picamera import PiCamera
from take_picture import take_picture
from PIL import Image
import io

class CameraCaptureStreamThread(Thread):
  def __init__(self, queue):
    self.queue = queue
    Thread.__init__(self)

  def run(self):
    with PiCamera(resolution = (144,96)) as c:
      stream = io.BytesIO()
      for foo in c.capture_continuous(stream, format='jpeg', use_video_port=True):
        # Truncate the stream to the current position (in case
        # prior iterations output a longer image)
        stream.truncate()
        stream.seek(0)
        img = Image.open(stream).load()
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

  def speed_test(self, delta):
    time.sleep(delta)
    count = 0
    try:
      while True:
        self.queue.get(block=False)
        count +=1
    except Empty:
      pass

    return count
    

if __name__ == "__main__":
  cam_stream = CameraCaptureStream()
  cam_stream.start()
  delta = 10
  count = cam_stream.speed_test(delta)
  print "{} images over {} seconds. {} ips".format(count, delta, float(count)/delta)
  # last_img = None
  # while True:
  #   new_img = cam_stream.get_latest_image()
  #   if (new_img == last_img):
  #     print "Same"
  #   last_img = new_img
  #   time.sleep(.1)
