import math
import colorsys
from PIL import Image

SIZE_DIFF = .3
PROXIMITY = 0.41
HUE_LOWER = .12
HUE_UPPER = .23
SAT_LOWER = .3
SAT_UPPER = .7
VAL_LOWER = 30
VAL_UPPER = 165

SPLITS_X = 9
SPLITS_Y = 14

#Splits and image in squares
def split_image(image_path, split_x=None, split_y=None, split_save_path=None):
    #ext = image_path.split(".")[-1]
    #img = Image.open(image_path)
    img = image_path
    (imageWidth, imageHeight)=image_path.size

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

            # if not split_save_path == None:
            #     slice_bit.save('{}/xmap_{}_{}.{}'.format(split_save_path, x, y, ext), optimize=True, bits=6)
        if len(split_grid_y) > 0:
            split_grid.append(split_grid_y)
    return (imageWidth, imageHeight), split_grid

#Check of a given RGB color is within the green color spectrum
def close_to_green(color, (hue_lower, hue_upper, sat_lower, sat_upper, val_lower, val_upper)):
    hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
    hue_treshold = [hue_lower, hue_upper]
    sat_treshold = [sat_lower, sat_upper]
    val_treshold = [val_lower, val_upper]

#    print hue_treshold, sat_treshold, val_treshold

    valid_hue = hsv[0] <= hue_treshold[1] and hsv[0] >= hue_treshold[0]
    valid_sat = hsv[1] <= sat_treshold[1] and hsv[1] >= sat_treshold[0]
    valid_val = hsv[2] <= val_treshold[1] and hsv[2] >= val_treshold[0]


    r = False
    if valid_hue and valid_sat and valid_val:
        r = True
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

def average_color(image):
    w, h = image.size
    pixels = image.getcolors(w * h)

    counts = 0
    r, g, b = 0, 0, 0

    for count, colour in pixels:
        if count > 1:
            r += colour[0]*count
            g += colour[1]*count
            b += colour[2]*count
            counts += count

    average_color = (r/counts, g/counts, b/counts) if counts > 0 else (0,0,0)

    return (counts, average_color)

# Checks if a section of an image is clear
def analyze_section(splits, start, stop, (proximity, size_diff)):
    mx = stop - start
    my = len(splits[0])
    
    green_in_row = []

    for y in reversed(range(my)):
        n_green = 0
        for x in range(start, stop):
            split = splits[x][y]
            close = split['is_green']
            if not close:
                n_green += 1
        green_in_row.append(n_green)


    proximity_limit = math.ceil(proximity*my)
    size_limit = math.ceil(size_diff*mx)

    can_move = True
    for (i,p) in enumerate(green_in_row):
        if i < proximity_limit and p > size_limit:
            can_move = False
    
    return can_move, green_in_row, size_limit, proximity_limit

def stitch_colored_splits(splits, size):
    full_im = Image.new('RGB', size)
    for x in range(len(splits)):
        for y in range(len(splits[x])):
            split = splits[x][y]            
            im = Image.new('RGB', split['slice'].size, split['color'][1])
            full_im.paste(im, (split['xoffset'], split['yoffset']))
    return full_im

def stitch_green_splits(splits, size):
    full_im = Image.new('RGB', size)
    for x in range(len(splits)):
        for y in range(len(splits[x])):
            split = splits[x][y]            
            im = Image.new('RGB', split['slice'].size, (255, 255, 255) if split['is_green'] else (0,0,0))
            full_im.paste(im, (split['xoffset'], split['yoffset']))
    return full_im

#"Splits" the image into three parts and checks wether each part is free
def analyze_image(image, stitch = True, size_diff = SIZE_DIFF, proximity = PROXIMITY, hue_lower = HUE_LOWER,
    hue_upper = HUE_UPPER, sat_lower = SAT_LOWER, sat_upper = SAT_UPPER, val_lower = VAL_LOWER, 
    val_upper = VAL_UPPER, splits_x = SPLITS_X, splits_y = SPLITS_Y):


    _, splits = split_image(image, splits_x, splits_y)
    sec1 = int(math.floor(len(splits)/3))
    sec2 = 2 * sec1

    clear1, clear2, clear3 = False, False, False

    intermediate_images = []
    
    #Replace actual color with average color
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = average_color(split_y['slice'])

    if stitch:
        intermediate_images.append(stitch_colored_splits(splits, image.size))

    #Replace actual color with average color
    for split_x in splits:
        for split_y in split_x:
            split_y['is_green'] = close_to_green(
                split_y['color'][1],
                (hue_lower, hue_upper, sat_lower, sat_upper, val_lower, val_upper)
            )
    if stitch:
        intermediate_images.append(stitch_green_splits(splits, image.size))
    

    clear1, s1, s_limit1, p_limit1 = analyze_section(splits, 0, sec1, (proximity, size_diff))
    clear2, s2, s_limit2, p_limit2 = analyze_section(splits, sec1, sec2, (proximity, size_diff))
    clear3, s3, s_limit3, p_limit3 = analyze_section(splits, sec2, len(splits), (proximity, size_diff))

    # print s1
    # print s2
    # print s3
    return (clear1, clear2, clear3), intermediate_images

