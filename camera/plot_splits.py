from PIL import Image

def plot_image(size, splits, out):
    full_im = Image.new('RGB', size)
    for split in splits:
        im = Image.new('RGB', split['slice'].size, split['color'][1])
        full_im.paste(im, (split['xoffset'], split['yoffset']))

    full_im.save('{}/color.jpg'.format(out), optimize=True, bits=6)
