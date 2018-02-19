from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image

def takepicture()
# Create the in-memory stream
    stream = BytesIO()
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)

    size, splits = split_image(fp, split_x=25, split_y=25)
    colors = []
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = most_frequent_colour(split_y['slice'])



    outfile = 'assets/img.jpeg'
    plot_image(size, splits, outfile)
