'''
Sends steering commands over GPIO
'''
import RPi.GPIO as GPIO

def stop():
  chan_list = (5,13,26)
  GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

def right():
  chan_list = (5,13,26)
  GPIO.output(chan_list,(GPIO.HIGH,GPIO.HIGH,GPIO.LOW))

def left():
  chan_list = (5,13,26)
  GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))

def forward():
  chan_list = (5,13,26)
  GPIO.output(chan_list,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))

def back():
  chan_list = (5,13,26)
  GPIO.output(chan_list,(GPIO.LOW,GPIO.HIGH,GPIO.LOW))

def setup():
  GPIO.setmode(GPIO.BCM)
  chan_list = (5,13,26)
  GPIO.setup(chan_list,GPIO.OUT)
