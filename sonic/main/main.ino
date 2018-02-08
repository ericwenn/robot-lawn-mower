#include <Ultrasonic.h>


#define MIN_DISTANCE 25
#define FRONT_OFFSET 0
#define LEFT_OFFSET 0
#define RIGHT_OFFSET 0
#define REAR_OFFSET 0

#define FRONTSIG 14
#define LEFTSIG 15
#define RIGHTSIG 16
#define REARSIG 17
#define ERRORSIG 18
#define TRIG 12
#define TIMEOUT 40000UL
//Sensor declarations

Ultrasonic front(TRIG,11);
Ultrasonic frontLeft(TRIG,10, TIMEOUT);
Ultrasonic frontRight(TRIG,9, TIMEOUT);
Ultrasonic left(TRIG,8, TIMEOUT);
Ultrasonic right(TRIG,7, TIMEOUT);
Ultrasonic rear(TRIG,6, TIMEOUT);
Ultrasonic rearLeft(TRIG,5, TIMEOUT);
Ultrasonic rearRight(TRIG,4, TIMEOUT);

unsigned char signals;


void setup() {
  pinMode(FRONTSIG, OUTPUT); //FRONTSIG
  pinMode(LEFTSIG, OUTPUT); //LEFTSIG
  pinMode(RIGHTSIG, OUTPUT); //RIGHTSIG
  pinMode(REARSIG, OUTPUT); //REARSIG
  pinMode(ERRORSIG, OUTPUT); //ERRORSIG
  digitalWrite(FRONTSIG, LOW);
  signals = 0;

  //Used for debug
  Serial.begin(9600);
  Serial.println("Setup complete");
  
}

void loop() {
  signals = read_sensors(signals);
  update_signals(signals);

}

unsigned char read_sensors(char c){
  //Check front for hit, if hit _front = 1
  
  /* During de-bug
  unsigned char _front = determine_blocked(front) + determine_blocked(frontRight) + determine_blocked(frontLeft);

  //Check left and right
  unsigned char _left = determine_blocked(left);
  unsigned char _right = determine_blocked(right);
  
  unsigned char _rear = determine_blocked(rear) + determine_blocked(rearRight) + determine_blocked(rearLeft);
*/
  //De-bug

  //Serial.print(" FrontLeft: ");
  //Serial.print(determine_blocked(frontLeft));

    Serial.print(" Dist FrontRight: ");
  Serial.print(frontRight.distanceRead());

  delayMicroseconds(10);

Serial.print(" Dist Front: ");
  Serial.print(front.distanceRead());

  delayMicroseconds(10);

   Serial.print(" Dist FrontLeft: ");
  Serial.println(frontLeft.distanceRead());
  
//  c = _front | (_left << 1) | (_right << 2) | (_rear << 3);
  return c;
  
}

unsigned char determine_blocked(Ultrasonic sensor){
  unsigned char dist = sensor.distanceRead();
  //if 0, means its ito far away for the sensors
  if(dist < MIN_DISTANCE && dist != 0){
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

