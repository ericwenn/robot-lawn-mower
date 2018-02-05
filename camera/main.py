from image_splitter import split_image
from image_analyze import most_frequent_colour
from plot_splits import plot_image



size, splits = split_image("assets/ball-on-grass.jpeg", "assets/out")

colors = []
for split in splits:
    split['color'] = most_frequent_colour(split['slice'])

print splits

plot_image(size, splits, "assets/out")
