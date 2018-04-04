#import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty
from picamera import PiCamera
import camera


class CameraSensorThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.camera = camera.camera()

    def sensorCam(self, camera):
        return self.camera.get_picture_info(camera)

    def run(self):
        with PiCamera(resolution = (720,480)) as c:
            while(True):
                reading = self.sensorCam(c)
                event =  {
                    'can_move': reading,
                    'timestamp': time.time()
                    }
                self.queue.put(event)
                time.sleep(.5)



class CameraSensor(object):
    def __init__(self, port=8080):
        self.queue = Queue()
        self.stack = []
        self.thread = CameraSensorThread(self.queue)


    def start(self):
        self.thread.daemon = True
        self.thread.start()

    def get_ultrasound_events(self, n=1):
        # Read all events from sensors
        try:
            while True:
                event = self.queue.get(block=False)
                self.stack.append(event)
        except Empty:
            pass

        return self.stack[-n:]
