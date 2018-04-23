from time import time
import os
import math

DIR = 'stored_images'
FILE_LIMIT = 10

def ensure_dir_exists():
  if not os.path.exists(DIR):
    os.makedirs(DIR)

def store_image(image, variant, n_variants):
  ensure_dir_exists()
  path = "{}/{}.{}.jpg".format(DIR, int(time()), variant)
  image.save(path, optimize=True, bits=6)
  cleanup(FILE_LIMIT*n_variants)


def cleanup(limit):
  files = os.listdir(DIR)
  if len(files) <= limit:
    return

  files.sort()

  to_be_removed = files[:-limit]
  for f in to_be_removed:
    os.remove("{}/{}".format(DIR, f))
  
