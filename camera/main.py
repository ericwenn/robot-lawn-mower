from __future__ import division
from image_splitter import split_image
from image_analyze import most_frequent_colour
from plot_splits import plot_image
from colorsys import rgb_to_hsv




size, splits = split_image("assets/ball-on-grass.jpeg")

colors = []
for split in splits:
    split['color'] = most_frequent_colour(split['slice'])

plot_image(size, splits, "assets/")
