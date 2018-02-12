import RPi.GPIO as GPIO
import time

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
GPIO.setmode(GPIO.BCM)
chan_list = (17,22,27)
GPIO.setup(chan_list,GPIO.IN)
while True:
    if GPIO.input(17):
        print "Left"
    if GPIO.input(22):
        print "Right"
    if GPIO.input(27):
        print "Middle"
    time.sleep(0.5)
