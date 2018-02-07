#include <Ultrasonic.h>


#define MIN_DISTANCE 300
#define FRONT_OFFSET 0
#define LEFT_OFFSET 0
#define RIGHT_OFFSET 0
#define REAR_OFFSET 0

#define FRONTSIG 19
#define LEFTSIG 20
#define RIGHTSIG 21
#define REARSIG 22
#define ERRORSIG 23
//Sensor declarations

Ultrasonic front(15,14);
Ultrasonic frontLeft(15,13);
Ultrasonic frontRight(15,12);
Ultrasonic left(15,11);
Ultrasonic right(15,10);
Ultrasonic rear(15,9);
Ultrasonic rearLeft(15,8);
Ultrasonic rearRight(15,7);

unsigned char signals;




//Maybe we should let all sensors on each side use the same trigger pin to save pins, for example,
//All sensors mounted on the front can share trigger pin 13?

void setup() {
  pinMode(FRONTSIG, OUTPUT); //FRONTSIG
  pinMode(LEFTSIG, OUTPUT); //LEFTSIG
  pinMode(RIGHTSIG, OUTPUT); //RIGHTSIG
  pinMode(REARSIG, OUTPUT); //REARSIG
  pinMode(ERRORSIG, OUTPUT); //ERRORSIG
  signals = 0;
}

void loop() {
  signals = read_sensors(signals);
  update_signals(signals);
}

char read_sensors(char c){
  char front = determine_blocked(front) + determine_blocked(frontRight) + determine_blocked(frontLeft);
  char left = determine_blocked(left);
  char right = determine_blocked(right);
  char rear = determine_blocked(rear) + determine_blocked(rearRight) + determine_blocked(rearLeft);

  c = front | (left << 1) | (right << 2) | (rear << 3);
  return c;
  
}

char determine_blocked(Ultrasonic sensor){
  if(sensor.distanceRead() < MIN_DISTANCE){
    return 1; 
  }
  return 0;
}

void update_signals(char c){
  digitalWrite(FRONTSIG, (c & 0x00000001));
  digitalWrite(LEFTSIG, ((c & 0x00000010)>>1));
  digitalWrite(RIGHTSIG, ((c & 0x00000100)>>2));
  digitalWrite(REARSIG, ((c & 0x00001000)>>3));
}





