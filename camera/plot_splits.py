from PIL import Image

def plot_image(imageWidth, imageHeight, rangeX, rangeY, splits, frequent_pixels, out):
    full_im = Image.new('RGB', (imageWidth, imageHeight))
    i = 0

    x = 0
    y = 0
    for split in splits:
        im = Image.new('RGB', split.size, frequent_pixels[i][1])
        full_im.paste(im, (x, y))
        splitH, splitW = split.size
        y += splitH
        if (y + splitH) > imageHeight:
            y = 0
            x += splitW

        i += 1

    full_im.save('{}/color.jpg'.format(out), optimize=True, bits=6)
