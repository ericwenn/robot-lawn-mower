#ifndef lawn_mower_sesnors
#define lawn_mower_sensors

class Sensor{
  private:
    const unsigned char id;
    const unsigned char trig_pin;
    const unsigned char echo_pin;

  public:
    Sensor(unsigned char _id, unsigned char _trig_pin, unsigned char _echo_pin);
};

#endif

