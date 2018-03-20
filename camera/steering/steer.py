import RPi.GPIO as GPIO

def stop():
    chan_list = (26,13,5)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

def right():
    chan_list = (26,13,5)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.HIGH,GPIO.HIGH))

def left():
    chan_list = (26,13,5)
    GPIO.output(chan_list,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))
def forward():
    chan_list = (26,13,5)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))

def back():
    chan_list = (26,13,5)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.HIGH,GPIO.LOW))

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    chan_list = (5,13,26)
    GPIO.setup(chan_list,GPIO.OUT)
