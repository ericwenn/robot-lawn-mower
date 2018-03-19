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
    diff = (time.time() - self.raw_data[0]["timestamp"]) * 1000
    return max(0, 1 - (diff / FRESHNESS_LIMIT))

  def certainty(self):
    """
    U = number of sensors
    SENSOR_i(t) = value of sensor i at t timesteps ago
    T = number of timesteps to look back

    certainty_i = MAX(0, 1 - (SENSOR_i(0) - AVG(SENSOR_i(1..T))/2))
    certainty = certainty_0 * certainty_1 ... * certainty_U
    """

    number_of_readings = len(self.raw_data)

    if number_of_readings == 0:
      return 0

    number_of_sensors = len(self.raw_data[0]["can_move"])

    certainties = []
    for i in range(number_of_sensors):
      sum_readings = 0
      for reading in self.raw_data:
        sum_readings += 1 if reading["can_move"][i] else -1
      
      print "sum", sum_readings
      avg = float(sum_readings) / max(1, number_of_readings)
      print "avg", avg
      latest = 1 if self.raw_data[0]["can_move"][i] else -1 
      print "latest", latest 
      certainties.append(max(0, 1 - (latest - avg) / 2.0))
    
    print "certs", certainties
    return reduce(operator.mul, certainties)