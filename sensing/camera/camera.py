from io import BytesIO
from PIL import Image
from analyze_image import analyze_image


class Camera(object):


    def get_picture_info(self,camera):
        img = self.takePicture(camera)
        return analyze_image(img)

    #Between 0 and 1
    #proximity = 0.5
    #sizeDifference = 0.1

    #Uses the Pi camera to take a picture
    def takePicture(self,camera):
    	# Create the in-memory stream
    	stream = BytesIO()
    	#camera = PiCamera()
    	#with PiCamera(resolution=(720,480)) as camera:
    	camera.start_preview()
    	camera.capture(stream, format='jpeg', use_video_port = True)
    	# "Rewind" the stream to the beginning so we can read its content
    	stream.seek(0)
    	image = Image.open(stream)
    	return image
