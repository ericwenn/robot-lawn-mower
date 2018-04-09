import RPi.GPIO as GPIO
import time
from threading import Thread, Event
from Queue import Queue, Empty


class SoundSensorThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def sensorsLMR(self):
        pos = [True,True,True]
        if GPIO.input(17):
            pos[0]=False
        if GPIO.input(22):
            pos[2] = False
        if GPIO.input(27):
            pos[1] = False
        return pos

    def run(self):
        while(True):
            reading = self.sensorsLMR()
            event =  {
                'payload': {
                    'can_move': reading,
                },
                'timestamp': time.time()
            }
            self.queue.put(event)
            time.sleep(.5)



class SoundSensor(object):
    def __init__(self, port=8080):
        self.queue = Queue()
        self.stack = []
        self.thread = SoundSensorThread(self.queue)


    def start(self):
        GPIO.setmode(GPIO.BCM)
        chan_list = (17,22,27)
        GPIO.setup(chan_list,GPIO.IN)
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