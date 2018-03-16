from takePicture import *
#import image_splitter, image_analyze
from image_analyze import *
from image_splitter import *
from PIL import Image


#im = Image.open("testing.jpg")
#print(analyzeImage(im))


def getPictureInfo():
    image = takePicture()
    image.save("testing.jpeg",optimize=True,bits=6)
    return analyzeImage(image)
print getPictureInfo()
