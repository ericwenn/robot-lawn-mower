import time
import operator

# If a reading is less fresh than this value (in milliseconds) its considered to be unfresh.
FRESHNESS_LIMIT = 2000

class SensorReading(object):
  def freshness(self):
    """
    Defines how fresh this reading is.
    MAX(0, 1 - (diff / FRESHNESS_LIMIT))
    """
    raise NotImplementedError()
  
  def can_move_forward(self):
    """
    Defines if the sensors think its okay to move forward.
    returns float in interval [-1,1]
    """
    raise NotImplementedError()
  
  def time_window(self):
    raise NotImplementedError()

  def raw(self):
    raise NotImplementedError()


class UltraSoundSensorReading(SensorReading):
  """
  Expected raw reading format:
  [{
    timestamp: Date
    can_move: [ Bool, Bool, Bool ]
  }, ...]
  """
  def __init__(self, raw_data):
    self.raw_data = raw_data
  
  def freshness(self):
    return 1.0
    
    if len(self.raw_data) < 1:
      return 0

    diff = (time.time() - self.raw_data[-1]["timestamp"]) * 1000
    return max(0, 1 - (diff / FRESHNESS_LIMIT))

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

 
  def raw(self):
    return self.raw_data
    
  def time_window(self):
    first = self.raw_data[-1]
    last = self.raw_data[0]
    return first['timestamp'] - last['timestamp']

class CameraSensorReading(SensorReading):
  """
  """
  def __init__(self, raw_data):
    self.raw_data = raw_data
  
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

    
  def raw(self):
    return self.raw_data

  def time_window(self):
    first = self.raw_data[-1]
    last = self.raw_data[0]
    return first['timestamp'] - last['timestamp']
    

class GPSSensorReading(SensorReading):
  """
  """
  def __init__(self, raw_data):
    self.raw_data = raw_data
  
  def freshness(self):
    return 1.0    

  def certainty(self):
    return 1.0    

  def verdict(self):
    return -1.0
    
  def raw(self):
    return self.raw_data
