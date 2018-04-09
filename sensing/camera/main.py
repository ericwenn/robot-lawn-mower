from PIL import Image
from store_image import store_image

im = Image.open('testing.jpeg')
store_image(im)
print im