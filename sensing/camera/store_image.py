from time import time
import os


DIR = '.images'
FILE_LIMIT = 5

def ensure_dir_exists():
  if not os.path.exists(DIR):
    os.makedirs(DIR)

def store_image(image):
  ensure_dir_exists()
  path = "{}/{}.jpg".format(DIR, time())
  image.save(path, optimize=True, bits=6)
  cleanup()


def cleanup():
  files = os.listdir(DIR)
  if len(files) <= FILE_LIMIT:
    return

  files.sort()

  to_be_removed = files[FILE_LIMIT:]
  for f in to_be_removed:
    os.remove("{}/{}".format(DIR, f))
  