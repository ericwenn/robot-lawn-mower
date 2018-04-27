import matplotlib.pyplot as plt
from can_move_forward import can_move_forward
from persistant_readings import list_files
import json
from sensing.sensor_reading import CameraSensorReading, UltraSoundSensorReading, GPSSensorReading
from random import random
def rehydrate(path):
  d = json.load(open(path))
  uss = UltraSoundSensorReading(d['uss'])
  css = CameraSensorReading(d['css'])
  gss = GPSSensorReading(d['gsr'])

  return d['can_move'], uss, css, gss

def plot_verdicts():
  files = list_files()


  x = []
  y = []
  color = []
  scale = []
  for f in files:
    can_move, uss, css, gss = rehydrate(f)
    can_move_2, (us_verdict, cam_verdict) = can_move_forward(uss, css, gss)
    x.append(us_verdict)
    y.append(cam_verdict)
    if can_move and can_move_2:
      c = 'green'
      s = 10
    if (not can_move) and (not can_move_2):
      c = 'red'
      s = 10
    if can_move and (not can_move_2):
      c = 'yellow'
      s = 100
    if (not can_move) and can_move_2:
      c = 'orange'
      s = 100
    color.append( c)
    scale.append(s )

  
  plt.scatter(x,y,c=color, alpha=0.5, s=scale)
  plt.show()



if __name__ == '__main__':
  plot_verdicts()