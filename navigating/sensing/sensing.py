from webserver_thread import SensorListener
from sensor_reading import UltraSoundSensorReading
import time 

class Sensors(object):
  def __init__(self):
    self.sensor_listener = SensorListener()
    pass
  
  def start(self):
    self.sensor_listener.start()

  def get_ultrasound_readings(self):
    uls = UltraSoundSensorReading([{
      "timestamp": time.time(),
      "can_move": [ True, False, False]
    }])

    time.sleep(0.1)
    return uls



if __name__ == "__main__":
    sensors = Sensors()
    sensors.start()

    try:
        while True:
            ul = sensors.get_ultrasound_readings()
            print "Ultra sound", ul
            print "Freshness", ul.freshness()
            print "Certainty", ul.certainty()
            time.sleep(1)
    except KeyboardInterrupt:
        print "Shutting down webserver"
