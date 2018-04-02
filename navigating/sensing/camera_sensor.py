import time
from threading import Thread, Event
from Queue import Queue, Empty
from takePicture import *
from image_analyze import *
from PIL import Image


class CameraThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def get_picture_info(self):
        return analyzeImage(takePicture())

    def run(self):
        while(True):
            reading = self.get_picture_info()
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
        self.thread =CameraThread(self.queue)


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
