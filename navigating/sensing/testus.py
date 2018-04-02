import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
chan_list=(17,22,27)
GPIO.setup(chan_list,GPIO.IN)

while True:
	pos = [True, True, True]
	if GPIO.input(17):
		pos[2] = False
	if GPIO.input(22):
		pos[0] = False
	if GPIO.input(27):
		pos[1] = False
	print "pos", pos
	time.sleep(0.5)
