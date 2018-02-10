from image_splitter import split_image
from image_analyze import most_frequent_colour
from plot_splits import plot_image
import glob

infiles = set(glob.glob("assets/*")) - set(glob.glob("assets/*.out.*"))
for fp in infiles:
    size, splits = split_image(fp, split_x=25, split_y=25)
    colors = []
    for split_x in splits:
        for split_y in split_x:
            split_y['color'] = most_frequent_colour(split_y['slice'])


    fps = fp.split(".")
    fps[-1] = 'out.'+fps[-1]
    outfile = '.'.join(fps)
    plot_image(size, splits, outfile)
