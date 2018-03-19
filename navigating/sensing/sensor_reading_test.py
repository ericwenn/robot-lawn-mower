import unittest
from sensor_reading import UltraSoundSensorReading
import time

class TestUltraSoundReadings(unittest.TestCase):

  def test_certainty_no_data(self):
    raw_data = []
    usr = UltraSoundSensorReading(raw_data)

    self.assertLessEqual(usr.certainty(), .01)


  def test_certainty_little_data(self):
    raw_data = [{
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .3)


    


  def test_certainty_all_sensors_agreed(self):
    raw_data = [{
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertGreaterEqual(usr.certainty(), .9)

  def test_certainty_latest_data_doesnt_agreed(self):
    raw_data = [{
      "time_stamp": time.time(),
      "can_move": [ False, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }, {
      "time_stamp": time.time(),
      "can_move": [ True, True, True ]
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .2)