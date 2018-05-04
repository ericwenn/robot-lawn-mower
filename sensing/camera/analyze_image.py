'''
Image analysis algorithm. Given an image the algorithm decides whether its possible to move forward.
This decision is done for three different sections of the image; left, middle, right.
The algorithm uses color similarity (in HSV) to make these decisions.
'''
import math
import colorsys
from PIL import Image

# On a row in section, how big ratio needs to be grass for it to be considered "safe".
SIZE_DIFF = .4
# How close to the robot does the "unsafe" row for it to be impossible to move further ahead.
PROXIMITY = 0.2

# Upper and lower boundaries for hue, saturation and value.
# Used for deciding what grass or not.
HUE_LOWER = .1
HUE_UPPER = .42
SAT_LOWER = .35
SAT_UPPER = 1.0
VAL_LOWER = 0
VAL_UPPER = 260

# How many pixels to average the image over initially.
SPLITS_X = 14
SPLITS_Y = 9

def close_to_green(color):
  '''
  Color in rgb is converted to HSV and checked if its within grass boundaries
  '''
  hsv = colorsys.rgb_to_hsv(color[0] + 0.0, color[1] + 0.0, color[2] + 0.0)
  hue_treshold = [HUE_LOWER, HUE_UPPER]
  sat_treshold = [SAT_LOWER, SAT_UPPER]
  val_treshold = [VAL_LOWER, VAL_UPPER]

  valid_hue = hsv[0] <= hue_treshold[1] and hsv[0] >= hue_treshold[0]
  valid_sat = hsv[1] <= sat_treshold[1] and hsv[1] >= sat_treshold[0]
  valid_val = hsv[2] <= val_treshold[1] and hsv[2] >= val_treshold[0]

  r = False
  if valid_hue and valid_sat and valid_val:
    r = True
  return r, hsv

def analyze_section(splits, start, stop):
  '''
  Checks if a section of an image is clear
  '''
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

  proximity_limit = math.ceil(PROXIMITY*my)
  size_limit = math.ceil(SIZE_DIFF*mx)

  can_move = True
  for (i,p) in enumerate(green_in_row):
    if i < proximity_limit and p > size_limit:
      can_move = False
  
  return can_move, green_in_row, size_limit, proximity_limit

def stitch_green_splits(splits, size):
  '''
  Creates a PIL image from splits thats used for visualising algorithm.
  '''
  full_im = Image.new('RGB', size)
  for x in range(len(splits)):
    for y in range(len(splits[x])):
      split = splits[x][y]            
      im = Image.new('RGB', (1,1), (255, 255, 255) if split['is_green'] else (0,0,0))
      full_im.paste(im, (x, y))
  return full_im

def analyze_image(image):
  '''
  Checks if, given and image, its safe for the robot to continue driving.
  This is done in each of three sections; left, middle, right.
  '''
  intermediates = []
  resized = image.resize((SPLITS_X, SPLITS_Y), Image.BILINEAR)
  intermediates.append(('avg', resized))
  
  sec1 = int(math.floor(SPLITS_X/3))
  sec2 = 2 * sec1

  clear1, clear2, clear3 = False, False, False


  splits = []
  for x in range(SPLITS_X):
    split_x = []
    for y in range(SPLITS_Y):
      is_green, hsv = close_to_green(resized.getpixel((x,y)))
      split_x.append({
        'is_green': is_green,
        'hsv': hsv
      })
    splits.append(split_x)

  intermediates.append(('verdict', stitch_green_splits(splits, (SPLITS_X, SPLITS_Y))))

  clear1, s1, s_limit1, p_limit1 = analyze_section(splits, 0, sec1)
  clear2, s2, s_limit2, p_limit2 = analyze_section(splits, sec1, sec2)
  clear3, s3, s_limit3, p_limit3 = analyze_section(splits, sec2, len(splits))

  return (clear1, clear2, clear3), intermediates, splits

