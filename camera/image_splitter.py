from PIL import Image
import math



def split_image(image_path, split_x=None, split_y=None, split_save_path=None):
    #ext = image_path.split(".")[-1]
    #img = Image.open(image_path)
    img = image_path
    (imageWidth, imageHeight)=img.size

    rangex=split_x
    rangey=split_y

    gridx=int(math.ceil(float(imageWidth)/rangex))
    gridy=int(math.ceil(float(imageHeight)/rangey))


    split_grid = []


    for x in xrange(rangex):
        split_grid_y = []
        for y in xrange(rangey):
            x1 = min(x*gridx, imageWidth)
            x2 = min(x1+gridx, imageWidth)
            y1 = min(y*gridy, imageHeight)
            y2 = min(y1+gridy, imageHeight)

            if x1 == x2 or y1 == y2:
                continue
            bbox=(x1, y1, x2, y2)
            slice_bit=img.crop(bbox)

            split_grid_y.append({
                'slice': slice_bit,
                'xoffset': x1,
                'yoffset': y1
            })

            if not split_save_path == None:
                slice_bit.save('{}/xmap_{}_{}.{}'.format(split_save_path, x, y, ext), optimize=True, bits=6)
        if len(split_grid_y) > 0:
            split_grid.append(split_grid_y)
    return (imageWidth, imageHeight), split_grid
