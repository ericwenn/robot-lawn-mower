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

class CameraSensorThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def sensorCam(self, camera):
        img = take_picture(camera)
        reading, _ = analyze_image(img)
        return reading

    def send(self, reading):
        conn = httplib.HTTPConnection("cmg-navigating", "8080")
        body = json.dumps({ 'can_move': reading })
        conn.request("POST", "/camera", body, { 'Content-Type': 'application/json' })
        
    def run(self):
        with PiCamera(resolution = (720,480)) as c:
            while(True):
                reading = self.sensorCam(c)
                self.send(reading)
                time.sleep(.5)



class CameraSensor(object):
    def __init__(self, port=8080):
        self.thread = CameraSensorThread()


    def start(self):
        self.thread.daemon = True
        self.thread.start()




if __name__ == "__main__":
    cam_sense = CameraSensor()

    cam_sense.start()
    while True:
        time.sleep(.5)