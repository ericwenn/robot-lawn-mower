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
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .3)





  def test_certainty_all_sensors_agreed(self):
    raw_data = [{
      "timestamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "timestamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "timestamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "timestamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertGreaterEqual(usr.certainty(), .9)

  def test_certainty_latest_data_doesnt_agreed(self):
    raw_data = [{
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .5)

  def test_certainty_different_sensors(self):
    raw_data = [{
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, True, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, True, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, True, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, True, False ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertGreaterEqual(usr.certainty(), .9)
  
  def test_certainty_all_sensors_uncertain(self):
    raw_data = [{
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .3)

  
  def test_certainty_all_sensors_uncertain2(self):
    raw_data = [{
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertLessEqual(usr.certainty(), .5)
    self.assertGreaterEqual(usr.certainty(), .2)
  

  def test_certainty_all_sensors_uncertain3(self):
    raw_data = [{
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ False, False, False ] }
    }, {
      "time_stamp": time.time(),
      "payload": { "can_move": [ True, True, True ] }
    }]
    usr = UltraSoundSensorReading(raw_data)
    self.assertGreaterEqual(usr.certainty(), .5)