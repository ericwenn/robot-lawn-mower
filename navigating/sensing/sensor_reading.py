import time
import operator

class SensorReading(object):
  def __init__(self, raw_data):
    self.raw_data = raw_data

  def time_window(self):
    print "raw", self.raw_data
    first = self.raw_data[-1]
    last = self.raw_data[0]
    print "first", first
    print "last", last

    return first['timestamp'] - last['timestamp']
  
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
    """
    """
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
      for reading in self.raw_data[:4]:
        sum_readings += (1.0 if reading['payload']["can_move"][i] else -1.0)
      average = sum_readings / len(self.raw_data[:4])
      averages.append(average)
    
    return min(averages)


class GPSSensorReading(SensorReading):
  def can_move_forward(self):
    return 1.0
