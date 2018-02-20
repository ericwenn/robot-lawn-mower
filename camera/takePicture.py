from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from image_splitter import split_image
from plot_splits import plot_image
from image_analyze import *
import time

start = time.time()
# Create the in-memory stream
stream = BytesIO()
camera = PiCamera()
camera.start_preview()
#sleep(2)
while(True):
 camera.capture(stream, format='jpeg')
 # "Rewind" the stream to the beginning so we can read its content
 stream.seek(0)
 image = Image.open(stream)
 end = time.time()
 print (end -start)

 start = time.time()
 size, splits = split_image(image, split_x=25, split_y=25)
 colors = []
 for split_x in splits:
 	 for split_y in split_x:
        	 split_y['color'] = most_frequent_colour(split_y['slice'])



 outfile = 'img.jpeg'
 plot_image(size, splits, outfile)
 end = time.time()
 print (end - start)
