from __future__ import division
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from colorsys import rgb_to_hsv

def plot_image(size, splits, out):
    full_im = Image.new('RGB', size)
    draw = ImageDraw.Draw(full_im)
    fnt = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 20)

    for split in splits:
        im = Image.new('RGB', split['slice'].size, split['color'][1])
        full_im.paste(im, (split['xoffset'], split['yoffset']))
        #See if the hue is in the green range on HSV scale
        hue = rgb_to_hsv(split['color'][1][0]/255,split['color'][1][1]/255,split['color'][1][2]/255);
        if (150>hue[0]*360 >90) & (hue[1]>1/6):
            print(hue[1])
            draw.text((split['xoffset'], split['yoffset']),"Green",(0,0,0),fnt)
    full_im.save('{}/color.jpg'.format(out), optimize=True, bits=6)
