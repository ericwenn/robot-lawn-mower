from PIL import Image
from store_image import store_image
from analyze_image import analyze_image

im = Image.open('.images/1523282936.99.jpg')
an = analyze_image(im)
print an