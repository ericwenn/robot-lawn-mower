#include "lawn_mower_sensors.h"

Sensor::Sensor(unsigned char _id, unsigned char _trig_pin, unsigned char _echo_pin) : id(_id), trig_pin(_trig_pin), echo_pin(_echo_pin){};
