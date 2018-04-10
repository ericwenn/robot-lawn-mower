from PIL import Image
from analyze_image import analyze_image
from store_image import store_image
im = Image.open('.images/1523282922.65.jpg')
an, intermediate = analyze_image(im)
print intermediate[1]
store_image(im, 'in', 3)
store_image(intermediate[0], 'avg', 3)
store_image(intermediate[1], 'green', 3)
print an