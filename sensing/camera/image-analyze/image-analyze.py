from PIL import Image
from image_splitter import *
import math
import colorsys

#Between 0 and 1
proximity = 0.5
sizeDifference = 0.1

#Check of a given RGB color is within the green color spectrum
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
    #return hsv[0]*hsv[2]


#Analyze the pixels in an image and return the most frequent colur present
def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel


def analyzeSection(splits, start, stop):
    yCoord = 0
    breaks = False
    mx = stop - start
    my = len(splits[0])
    #Loop over the splits in given interval, see if any row is more than sizeDifference percent not green, record the y coordinate that
    #had the first anomaly, if that was under proximity return false otherwise return true
    for y in reversed(range(my)):
        perGreen =0;
        for x in range(start, stop):
            split = splits[x][y]
            close = closeness_to_green(split['color'][1])
            if close == 255:
                perGreen=perGreen +1
        if ((float(perGreen)/mx) > sizeDifference) and not breaks:
            yCoord = y +1
            breaks = True
    if breaks and float(yCoord)/my > proximity:
        return False
    return True


#"Splits" the image into three parts and checks wether each part is free
def analyzeImage(image):

    size, splits = split_image(image, split_x=25, split_y=25)
    sec1 = int(math.floor(len(splits)/3))
    sec2 = 2 * sec1

    clear1, clear2, clear3 = False, False, False

    #Replace actual color with avarage colour
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = most_frequent_colour(split_y['slice'])


    clear1 = analyzeSection(splits,0,sec1)
    clear2 = analyzeSection(splits,sec1,sec2)
    clear3 = analyzeSection(splits,sec2,len(splits))

    return (clear1, clear2, clear3)
