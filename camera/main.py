from image_splitter import split_image
from image_analyze import most_frequent_colour



splits = split_image("grass.jpg", "out")

for split in splits:
    print most_frequent_colour(split)
