import time
import operator

# If a reading is less fresh than this value (in milliseconds) its considered to be unfresh.
FRESHNESS_LIMIT = 2000

class SensorReading(object):
  def certainty(self):
    raise NotImplementedError()
  
  def freshness(self):
    """
    Defines how fresh this reading is.
    MAX(0, 1 - (diff / FRESHNESS_LIMIT))
    """
    raise NotImplementedError()
  
  def verdict(self):
    """
    Defines if the sensors think its okay to move forward.
    returns [-1,1]
    """
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

  def certainty(self):
    """
    U = number of sensors
    SENSOR_i(t) = value of sensor i at t timesteps ago
    T = number of timesteps to look back

    certainty_i = ABS(AVG(SENSOR_i(1..T)))
    certainty = certainty_0 * certainty_1 ... * certainty_U
    """

    number_of_readings = len(self.raw_data)

    if number_of_readings < 3:
      return 0

    number_of_sensors = len(self.raw_data[0]['payload']["can_move"])

    certainties = []
    gamma = .9
    for i in range(number_of_sensors):
      sum_readings = 0
      sum_gammas = 0
      _gamma = gamma
      for reading in self.raw_data[1:]:
        sum_readings += _gamma * (1 if reading['payload']["can_move"][i] else -1)
        sum_gammas += _gamma
        _gamma *= gamma
      latest_reading = 1 if self.raw_data[0]['payload']['can_move'][i] else -1
      diff = abs((sum_readings / sum_gammas) - latest_reading) / 2
      print sum_readings, sum_gammas, diff
      certainties.append(1 - diff)
    
    return min(certainties)
    return reduce(lambda x, y: x + y, certainties) / len(certainties)
    #return reduce(operator.mul, certainties)

  def verdict(self):

    if len(self.raw_data) < 1:
      return 1

    can_move = True
    for verdict_i in self.raw_data[-1]['payload']["can_move"]:
      if not verdict_i:
        can_move = False
    
    return 1 if can_move else -1

  
  def raw(self):
    return self.raw_data

class CameraSensorReading(SensorReading):
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


class GPSSensorReading(SensorReading):
  """
  """
  def __init__(self, raw_data):
    self.raw_data = raw_data
  
  def freshness(self):
    raise NotImplementedError()

  def certainty(self):
    raise NotImplementedError()
  
  def verdict(self):
    raise NotImplementedError()