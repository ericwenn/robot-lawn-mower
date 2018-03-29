from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image


class camera(object):



    def get_picture_info(self):
        return self.analyzeImage(self.takePicture())
    #Between 0 and 1
    proximity = 0.5
    sizeDifference = 0.1

    #Uses the Pi camera to take a picture
    def takePicture():
    	# Create the in-memory stream
    	stream = BytesIO()
    	#camera = PiCamera()
    	with PiCamera(resolution=(720,480)) as camera:
    		camera.start_preview()
    		camera.capture(stream, format='jpeg', use_video_port = True)
    	# "Rewind" the stream to the beginning so we can read its content
    	stream.seek(0)
    	image = Image.open(stream)
    	return image

    #Splits and image in squares
    def split_image(image_path, split_x=None, split_y=None, split_save_path=None):
        #ext = image_path.split(".")[-1]
        #img = Image.open(image_path)
        img = image_path
        (imageWidth, imageHeight)=img.size

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

                if not split_save_path == None:
                    slice_bit.save('{}/xmap_{}_{}.{}'.format(split_save_path, x, y, ext), optimize=True, bits=6)
            if len(split_grid_y) > 0:
                split_grid.append(split_grid_y)
        return (imageWidth, imageHeight), split_grid

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

    #Checks if a section of an image is clear
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
                close = self.closeness_to_green(split['color'][1])
                if not close:
                    perGreen=perGreen +1
            if ((float(perGreen)/mx) > sizeDifference) and not breaks:
                yCoord = y +1
                breaks = True
        if breaks and float(yCoord)/my > proximity:
            return False
        return True


    #"Splits" the image into three parts and checks wether each part is free
    def analyzeImage(image):

        size, splits = self.split_image(image, split_x=25, split_y=25)
        sec1 = int(math.floor(len(splits)/3))
        sec2 = 2 * sec1

        clear1, clear2, clear3 = False, False, False

        #Replace actual color with avarage colour
        for split_x in splits:
            for split_y in split_x:
                split_y['color'] = self.most_frequent_colour(split_y['slice'])


        clear1 = self.analyzeSection(splits,0,sec1)
        clear2 = self.analyzeSection(splits,sec1,sec2)
        clear3 = self.analyzeSection(splits,sec2,len(splits))

        return (clear1, clear2, clear3)
