from can_move_forward import can_move_forward
from persistant_readings import list_files
import json
from sensing.sensor_reading import CameraSensorReading, UltraSoundSensorReading, GPSSensorReading
files = list_files()

def rehydrate(path):
  d = json.load(open(path))
  uss = UltraSoundSensorReading(d['uss'])
  css = CameraSensorReading(d['css'])
  gss = GPSSensorReading(d['gsr'])

  return d['can_move'], uss, css, gss


correct = 0
incorrect = 0
false_positive = 0

mm = {}


for f in files:
  can_move, uss, css, gss = rehydrate(f) 
  can_move_2 = can_move_forward(uss, css, gss)

  print 'uss'
  print uss.time_window()
  print 'camera'
  print css.time_window()

  key = "{} {}".format(can_move, can_move_2)
  if not key in mm:
    mm[key] = 0
  
  mm[key] += 1
  if can_move == can_move_2:
    correct += 1
  else:
    if can_move_2:
      false_positive += 1
    incorrect += 1
print mm
print "Tested {} slices. {} slices were correct. {}%".format(correct + incorrect, correct, float(correct*100) / (correct + incorrect))
print "False positives {}. {}%".format(false_positive, float(false_positive*100) / (incorrect))