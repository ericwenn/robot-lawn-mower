from PIL import Image
from analyze_image import analyze_image, split_image, SPLITS_X, SPLITS_Y, average_color, close_to_green, HUE_LOWER, HUE_UPPER, SAT_LOWER, SAT_UPPER, VAL_LOWER, VAL_UPPER
from test_images import test_images

imgs = []
for (img_path, actual) in test_images[:10]:
  imgs.append(Image.open(img_path))

size, splits = split_image(imgs[0], SPLITS_X, SPLITS_Y)


for split_x in splits:
  for split_y in split_x:
      split_y['color'] = average_color(split_y['slice'])


def test_full():
  for i in range(10):
    for img in imgs:
      _ = analyze_image(img, stitch = False)


def test_split():
  for i in range(10):
    for img in imgs:
      _ = split_image(img, SPLITS_X, SPLITS_Y)

def test_avg():
  for i in range(100):
    for split_x in splits:
        for split_y in split_x:
            _ = average_color(split_y['slice'])

def test_is_green():
  for i in range(100):
    for split_x in splits:
      for split_y in split_x:
          split_y['is_green'] = close_to_green(
              split_y['color'][1],
              (HUE_LOWER, HUE_UPPER, SAT_LOWER, SAT_UPPER, VAL_LOWER, VAL_UPPER)
          )

if __name__ == '__main__':
    import timeit
    s = timeit.timeit("test_full()", setup="from __main__ import test_full", number=1)
    print "{} analyzes per second".format(100/s)


    s = timeit.timeit("test_split()", setup="from __main__ import test_split", number=1)
    print "{} splits per second".format(100/s)

    s = timeit.timeit("test_avg()", setup="from __main__ import test_avg", number=1)
    print "{} averages per second".format(100/s)

    s = timeit.timeit("test_is_green()", setup="from __main__ import test_is_green", number=1)
    print "{} is green checks per second".format(100/s)

    