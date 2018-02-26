from PIL import Image
SPLIT_X=50
SPLIT_Y=50


def split_image(image_path, split_save_path=None):
    ext = image_path.split(".")[-1]
    img = Image.open(image_path)
    (imageWidth, imageHeight)=img.size
    gridx=SPLIT_X
    gridy=SPLIT_Y
    rangex=imageWidth/gridx
    rangey=imageHeight/gridy

    splits = []

    for x in xrange(rangex):
        for y in xrange(rangey):
            bbox=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
            slice_bit=img.crop(bbox)

            splits.append(slice_bit)

            if not split_save_path == None:
                slice_bit.save('{}/xmap_{}_{}.{}'.format(split_save_path, x, y, ext), optimize=True, bits=6)
                print 'out/xmap_'+str(x)+'_'+str(y)+'.png'

    return splits

print split_image("color-grid.jpg", "out")
