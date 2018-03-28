from takePicture import *
from image_analyze import *
from PIL import Image

def getPictureInfo():
    image = takePicture()
    image.save("testing.jpeg",optimize=True,bits=6)
    return analyzeImage(image)
print getPictureInfo()
