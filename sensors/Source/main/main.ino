#include <lawn_mower_sensors.h>
#include <hcsr04.h>

//Sensor declarations
Sensor front(1,13,14);
Sensor frontRight(2,12,11);
Sensor frontLeft(3,10,9);
Sensor left(4,8,7);
Sensor right(5,6,5);
Sensor rear(6,4,3);

//Maybe we should let all sensors on each side use the same trigger pin to save pins, for example,
//All sensors mounted on the front can share trigger pin 13?

void setup() {
  
}

void loop() {
  // put your main code here, to run repeatedly:

}





