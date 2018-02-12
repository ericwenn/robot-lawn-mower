from PIL import Image
import math
import colorsys

def closeness_to_gray(color):
    hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
    hue_treshold = [0, 1]
    sat_treshold = [0, .4]
    val_treshold = [5, 150]

    valid_hue = hsv[0] <= hue_treshold[1] and hsv[0] >= hue_treshold[0]
    valid_sat = hsv[1] <= sat_treshold[1] and hsv[1] >= sat_treshold[0]
    valid_val = hsv[2] <= val_treshold[1] and hsv[2] >= val_treshold[0]


    r = 255
    if valid_hue and valid_sat and valid_val:
        r = 0
    #print valid_hue, valid_sat, valid_val, hsv
    return r

def closeness_to_green(color):
    hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
    hue_treshold = [0.1, 0.5]
    sat_treshold = [0.15, 1]
    val_treshold = [15, 250]

    valid_hue = hsv[0] <= hue_treshold[1] and hsv[0] >= hue_treshold[0]
    valid_sat = hsv[1] <= sat_treshold[1] and hsv[1] >= sat_treshold[0]
    valid_val = hsv[2] <= val_treshold[1] and hsv[2] >= val_treshold[0]


    r = 255
    if valid_hue and valid_sat and valid_val:
        r = 0
    #print valid_hue, valid_sat, valid_val, hsv
    return r
    return hsv[0]*hsv[2]



def plot_image(size, splits, between, out):
    full_im = Image.new('RGB', size)
    between_im = Image.new('RGB', size)
    mx = len(splits)
    my = len(splits[0])
    for x in range(mx):
        for y in range(my):
            split = splits[x][y]
            close = closeness_to_green(split['color'][1])
            im = Image.new('RGB', split['slice'].size, (close, 0, 0))
            b_im = Image.new('RGB', split['slice'].size, split['color'][1])

            between_im.paste(b_im, (split['xoffset'], split['yoffset']))
            full_im.paste(im, (split['xoffset'], split['yoffset']))

    print between
    full_im.save(out, optimize=True, bits=6)
    between_im.save(between, optimize=True, bits=6)
