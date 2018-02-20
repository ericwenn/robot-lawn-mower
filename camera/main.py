from image_splitter import split_image
from image_analyze import most_frequent_colour, average_colour
from plot_splits import plot_image
import glob

infiles = set(glob.glob("assets/*")) - set(glob.glob("assets/*.zout.*"))
#infiles = ["assets2/IMG_4005.JPG"]
for fp in infiles:
    size, splits = split_image(fp, split_x=100, split_y=100)
    colors = []
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = average_colour(split_y['slice'])


    fps = fp.split(".")
    fps[-1] = 'zout.'+fps[-1]
    outfile = '.'.join(fps)
    fps[-1] = 'zbetween.'+fps[-1]
    betweenfile = '.'.join(fps)
    plot_image(size, splits, betweenfile, outfile)
