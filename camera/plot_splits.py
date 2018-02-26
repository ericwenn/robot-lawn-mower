from PIL import Image, ImageDraw
import math
import colorsys

#Between 0 and 1
proximity = 0.65

def closeness_to_green(color):
    hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
    green = (0, 255, 0)
    diff = (green[0] - color[0], green[1] - color[1], green[2] - color[2])
    hue_treshold = [0.1, 0.55]
    sat_treshold = [0.15, 1]
    val_treshold = [10, 250]

    valid_hue = hsv[0] <= hue_treshold[1] and hsv[0] >= hue_treshold[0]
    valid_sat = hsv[1] <= sat_treshold[1] and hsv[1] >= sat_treshold[0]
    valid_val = hsv[2] <= val_treshold[1] and hsv[2] >= val_treshold[0]


    r = 255
    if valid_hue and valid_sat and valid_val:
        r = 0
    #print valid_hue, valid_sat, valid_val, hsv
    return r
    return hsv[0]*hsv[2]



def plot_image(size, splits, out):
    full_im = Image.new('RGB', size)
    mx = len(splits)
    my = len(splits[0])
    breaks = False
    yCoord = size[1]
    for y in reversed(range(my)):
        perGreen =1;
        for x in range(mx):
            split = splits[x][y]
            close = closeness_to_green(split['color'][1])
            if close == 0:
                perGreen=perGreen +1
            #im = Image.new('RGB', split['slice'].size, (close, 0, 0))
            im = Image.new('RGB', split['slice'].size, split['color'][1])

            full_im.paste(im, (split['xoffset'], split['yoffset']))
        #If the number if green splits in a row is smaller than a percentage, record that y coordinate
        if ((float(perGreen)/mx) < 0.8) and not breaks:
            yCoord = split['yoffset']
            breaks = True

    if breaks:
        draw = ImageDraw.Draw(full_im)
        draw.line((0,yCoord,size[0],yCoord),fill=0,width=10)
        if float(yCoord)/size[1] > proximity:
            print "To close!"
            print out
            print ""

    full_im.save(out, optimize=True, bits=6)
