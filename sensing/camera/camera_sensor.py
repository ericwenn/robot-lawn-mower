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
class CameraSensorThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def sensorCam(self, camera):
        img = take_picture(camera)
        reading, _ = analyze_image(img)
        reading, intermediate = analyze_image(img)
        store_image(img, 'in', 3)
        store_image(intermediate[0], 'avg', 3)
        store_image(intermediate[1], 'green', 3)
        return reading

    def send(self, reading):
        conn = httplib.HTTPConnection("cmg-navigating", "8080")
        body = json.dumps({ 'can_move': reading })
        try:
            conn.request("POST", "/camera", body, { 'Content-Type': 'application/json' })
            conn.getresponse()
        except:
            pass
        
    def run(self):
        with PiCamera(resolution = (144,96)) as c:
            while(True):
                reading = self.sensorCam(c)
                self.send(reading)
                time.sleep(0.05)



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
        time.sleep(.5)