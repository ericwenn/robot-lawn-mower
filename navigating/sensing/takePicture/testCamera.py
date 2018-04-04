from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
import camera

'''
def takePicture():
	# Create the in-memory stream
	stream = BytesIO()
	#camera = PiCamera()
	with PiCamera(resolution=(720,480)) as camera:
		camera.start_preview()
		camera.capture(stream, format='jpeg', use_video_port = True)
	# "Rewind" the stream to the beginning so we can read its content
	stream.seek(0)
	image = Image.open(stream)
	return image
'''
cam = camera.camera()
with PiCamera(resolution = (720,480)) as c:
	try:
		while True:
        	print cam.get_picture_info(c)
        	sleep(0.5)
	except KeyboardInterrupt:
        print "User cancelled"
