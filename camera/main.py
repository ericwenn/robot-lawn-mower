from image_splitter import split_image
from image_analyze import most_frequent_colour
from plot_splits import plot_image
import glob
import RPi.GPIO as GPIO
from soundsensor import *
from steer import *


#infiles = set(glob.glob("assets/*")) - set(glob.glob("assets/*.out.*"))
#for fp in infiles:
#    size, splits = split_image(fp, split_x=25, split_y=25)
#    colors = []
#    for split_x in splits:
#        for split_y in split_x:
#            split_y['color'] = most_frequent_colour(split_y['slice'])
#
#
#    fps = fp.split(".")
#    fps[-1] = 'out.'+fps[-1]
#    outfile = '.'.join(fps)
#    plot_image(size, splits, outfile)
#GPIO.setmode(GPIO.BCM)
#chan_list = (17,22,27)
#GPIO.setup(chan_list,GPIO.IN)
#while True:
#    if GPIO.input(17):
#        print "Left"
#    if GPIO.input(22):
#        print "Right"
#    if GPIO.input(27):
#        print "Middle"


setupGPIO()
setup()

while(True):
    pos = sensorsLMR()
    if(pos[0] && pos[1] && pos[2]):
        stop()
    elif((pos[0] && pos[1] && !pos[2]):
        right()
    elif(!pos[0] && pos[1] && pos[2]):
        left()
    elif(!pos[0] && !pos[1] && !pos[2]):
        forward()
