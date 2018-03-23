import RPi.GPIO as GPIO

def stop():
    chan_list = (5,13,26)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

def right():
    #print "Going right"    
    chan_list = (5,13,26)
    GPIO.output(chan_list,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))

def left():
    #print "Going left"    
    chan_list = (5,13,26)
    GPIO.output(chan_list,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))

def forward():
    #print "Going forward"        
    chan_list = (5,13,26)
    GPIO.output(chan_list,(GPIO.HIGH,GPIO.LOW,GPIO.HIGH))

def back():
    #print "Going backward"        
    chan_list = (5,13,26)
    GPIO.output(chan_list,(GPIO.HIGH,GPIO.HIGH,GPIO.HIGH))

def setup():
    GPIO.setmode(GPIO.BCM)
    chan_list = (5,13,26)
    GPIO.setup(chan_list,GPIO.OUT)



if __name__ == "__main__":
    setup()
    stop()