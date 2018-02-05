from image_splitter import split_image
from image_analyze import most_frequent_colour
from plot_splits import plot_image



imageWidth, imageHeight, rangex, rangey, splits = split_image("assets/grass.jpg", "assets/out")

colors = []
for split in splits:
    colors.append(most_frequent_colour(split))


plot_image(imageWidth, imageHeight, rangex, rangey, splits, colors, "assets/out")
