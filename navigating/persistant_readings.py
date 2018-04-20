from time import time
import os
import math
import json

DIR = 'stored_readings'
FILE_LIMIT = 1000

def ensure_dir_exists():
  if not os.path.exists(DIR):
    os.makedirs(DIR)

def store_reading(uss, css, gsr, can_move):
  ensure_dir_exists()
  
  data = {
    'uss': uss.raw(),
    'css': css.raw(),
    'gsr': gsr.raw(),
    'can_move': can_move
  }
  print data

  # path = "{}/{}.json".format(DIR, int(time()*1000))
  # with open(path, 'w') as outfile:
  #   json.dump(data, outfile)
  # image.save(path, optimize=True, bits=6)
  # cleanup(FILE_LIMIT*n_variants)


def cleanup(limit):
  files = os.listdir(DIR)
  if len(files) <= limit:
    return

  files.sort()

  to_be_removed = files[:-limit]
  for f in to_be_removed:
    os.remove("{}/{}".format(DIR, f))
  
