from PIL import Image

def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)
    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    # compare("Most Common", image, most_frequent_pixel[1])

    return most_frequent_pixel


def average_colour(image):
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
