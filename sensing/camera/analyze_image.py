import math
import colorsys
from PIL import Image

sizeDifference = 0.1
proximity = 0.5

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
def close_to_green(color):
    hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
    green = (0, 255, 0)
    diff = (green[0] - color[0], green[1] - color[1], green[2] - color[2])
    hue_treshold = [0.1, 0.55]
    sat_treshold = [0.15, 1]
    val_treshold = [10, 250]

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
    rgb = (0,0,0)

    for count, colour in pixels:
        weighted_color = (colour[0]*count, colour[1]*count, colour[2]*count)
        rgb = tuple(map(sum,zip(rgb,weighted_color)))
        counts += count
    # compare("Most Common", image, most_frequent_pixel[1])
    average_color = ( rgb[0]/counts, rgb[1] /counts, rgb[2]/counts)
    #print average_color

    return (counts, average_color)

# Checks if a section of an image is clear
def analyze_section(splits, start, stop):
    yCoord = 0
    breaks = False
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
    size_limit = math.ceil(sizeDifference*mx)

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
def analyze_image(image):

    size, splits = split_image(image, 36, 36)
    sec1 = int(math.floor(len(splits)/3))
    sec2 = 2 * sec1

    clear1, clear2, clear3 = False, False, False

    intermediate_images = []
    
    #Replace actual color with average color
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = average_color(split_y['slice'])

    intermediate_images.append(stitch_colored_splits(splits, image.size))

    #Replace actual color with average color
    for split_x in splits:
        for split_y in split_x:
            split_y['is_green'] = close_to_green(split_y['color'][1])

    intermediate_images.append(stitch_green_splits(splits, image.size))
    

    clear1, s1, s_limit1, p_limit1 = analyze_section(splits, 0, sec1)
    clear2, s2, s_limit2, p_limit2 = analyze_section(splits, sec1, sec2)
    clear3, s3, s_limit3, p_limit3 = analyze_section(splits, sec2, len(splits))

    print clear1, s1, s_limit1, p_limit1
    print clear2, s2, s_limit2, p_limit2
    print clear3, s3, s_limit3, p_limit3
    print ""
    #clear3 = self.analyzeSection(splits,sec2,len(splits))

    return (clear1, clear2, clear3), intermediate_images

