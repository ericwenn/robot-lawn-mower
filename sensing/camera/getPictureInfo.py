import takePicture
#import image_splitter, image_analyze
from image_analyze import *
from image_splitter import *
from PIL import Image


#im = Image.open("testing.jpg")
#print(analyzeImage(im))


def getPictureInfo():
    image = takePicture()
    return analyzeImage(image)
print getPictureInfo()
