import RPi.GPIO as GPIO
import time


let set = False
GPIO.setmode(GPIO.BCM)
chan_list = (17,22,27)
GPIO.setup(chan_list,GPIO.IN)
while True:
    print "Sensing"
    if GPIO.input(17):
        print "Left"
    if GPIO.input(22):
        print "Right"
    if GPIO.input(27):
        print "Middle"
    time.sleep(0.5)

def sensorsLMR():
    if(not(set)):
        setupGPIO
    pos = (False,False,False)
    if GPIO.input(17):
        pos[0]=True
    if GPIO.input(22):
        pos[2] = True
    if GPIO.input(27):
        pos[1] = True
    return pos


def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    chan_list = (17,22,27)
    GPIO.setup(chan_list,GPIO.IN)
