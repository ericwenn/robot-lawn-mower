from PIL import Image
import math
SPLIT_X=150
SPLIT_Y=150


def split_image(image_path, split_save_path=None):
    ext = image_path.split(".")[-1]
    img = Image.open(image_path)
    (imageWidth, imageHeight)=img.size
    gridx=SPLIT_X
    gridy=SPLIT_Y

    rangex=int(math.ceil(float(imageWidth)/gridx))
    rangey=int(math.ceil(float(imageHeight)/gridy))
    print rangex

    splits = []

    for x in xrange(rangex):
        for y in xrange(rangey):
            x1 = x*gridx
            x2 = min(x1+gridx, imageWidth)
            y1 = y*gridy
            y2 = min(y1+gridy, imageHeight)
            bbox=(x1, y1, x2, y2)
            slice_bit=img.crop(bbox)

            splits.append({
                'slice': slice_bit,
                'xoffset': x1,
                'yoffset': y1
            })

            if not split_save_path == None:
                slice_bit.save('{}/xmap_{}_{}.{}'.format(split_save_path, x, y, ext), optimize=True, bits=6)

    return (imageWidth, imageHeight), splits
