from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image


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
