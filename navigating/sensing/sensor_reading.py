'''
Classes for working with sensors readings in a normalized way.
'''
import time
import operator

class SensorReading(object):
  def __init__(self, raw_data):
    self.raw_data = raw_data

  def time_window(self):
    if len(self.raw_data) < 1:
      return 0.0
    first = self.raw_data[-1]
    last = self.raw_data[0]

    window = first['timestamp'] - last['timestamp']
    return float("%.3f"%window)
  
  def can_move_forward(self):
    """
    Defines if the sensors think its okay to move forward.
    returns float in interval [-1,1]
    """
    raise NotImplementedError()
  
  def raw(self):
    return self.raw_data


class UltraSoundSensorReading(SensorReading):
  """
  Expected raw reading format:
  [{
    timestamp: Date
    can_move: [ Bool, Bool, Bool ]
  }, ...]
  """
  def can_move_forward(self):
    number_of_readings = len(self.raw_data)

    if number_of_readings < 3:
      return -1.0

    number_of_sensors = len(self.raw_data[0]['payload']["can_move"])

    averages = []
    for i in range(number_of_sensors):
      sum_readings = 0
      for reading in self.raw_data:
        sum_readings += (1.0 if reading['payload']["can_move"][i] else -1.0)
      average = sum_readings / len(self.raw_data)
      averages.append(average)
    
    return min(averages)
    


class CameraSensorReading(SensorReading):

  def can_move_forward(self):
    number_of_readings = len(self.raw_data)

    if number_of_readings < 3:
      return -1.0

    number_of_sensors = len(self.raw_data[0]['payload']["can_move"])

    averages = []
    for i in range(number_of_sensors):
      sum_readings = 0
      for reading in self.raw_data:
        sum_readings += (1.0 if reading['payload']["can_move"][i] else -1.0)
      average = sum_readings / len(self.raw_data)
      averages.append(average)
    
    return min(averages)


class GPSSensorReading(SensorReading):
  def can_move_forward(self):
    number_of_readings = len(self.raw_data)
    if number_of_readings < 3:
      return 1.0

    verdict = self.raw_data[-1]['payload']['isInside']
    is_configured = self.raw_data[-1]['payload']['configured']

    if not is_configured:
      return 1.0
    
    return 1.0 if verdict else -1.0
