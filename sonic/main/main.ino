#include <Ultrasonic.h>

#define DEBUG

#define MAX_DISTANCE 25

#define LEFTSIG 14
#define FRONTSIG 15
#define RIGHTSIG 16
#define REARSIG 17
#define ERRORSIG 18

#define TRIG_LEFT 12
#define TRIG_FRONT 11
#define TRIG_RIGHT 10
#define TIMEOUT 40000UL

//Sensor declarations

Ultrasonic frontLeft(TRIG_LEFT,9, TIMEOUT);
Ultrasonic frontFront(TRIG_FRONT,8,TIMEOUT);;
Ultrasonic frontRight(TRIG_RIGHT,7, TIMEOUT);
//Ultrasonic left(TRIG,8, TIMEOUT);
//Ultrasonic right(TRIG,7, TIMEOUT);
//Ultrasonic rear(TRIG,6, TIMEOUT);
//Ultrasonic rearLeft(TRIG,5, TIMEOUT);
//Ultrasonic rearRight(TRIG,4, TIMEOUT);


void setup() {
  pinMode(LEFTSIG, OUTPUT); //LEFTSIG
  pinMode(FRONTSIG, OUTPUT); //FRONTSIG
  pinMode(RIGHTSIG, OUTPUT); //RIGHTSIG
  pinMode(REARSIG, OUTPUT); //REARSIG
  pinMode(ERRORSIG, OUTPUT); //ERRORSIG

  #ifdef DEBUG
    Serial.begin(9600);
  #endif
}

void loop() {
  check_sensors();
}

void check_sensors(){
  
  //Read sensors and trigger relevant signal pin if blocked
  //FRONT
  unsigned char _frontLeft = frontLeft.distanceRead();
  delay(4);
  unsigned char _frontFront = frontFront.distanceRead();
  delay(4);
  unsigned char _frontRight = frontRight.distanceRead();
  digitalWrite(FRONTSIG, (determine_blocked(_frontFront) | determine_blocked(_frontRight) | determine_blocked(_frontLeft)));
  delay(4);
  
  //LEFT
  //RIGHT
  //REAR
  
  #ifdef DEBUG
    //If you use a smart serial monitor (like putty) these two lines will do you good
    Serial.print("\033[2j");
    Serial.print("\033[H");
    
    Serial.print("FrontLeft ");
    Serial.print(_frontLeft);
    Serial.print(" ");
    Serial.println(determine_blocked(_frontFront));
  
    Serial.print("FrontFront ");
    Serial.print(_frontFront);
    Serial.print(" ");
    Serial.println(determine_blocked(_frontRight));
  
    Serial.print("FrontRight ");
    Serial.print(_frontRight);
    Serial.print(" ");
    Serial.println(determine_blocked(_frontLeft));
    Serial.println("");

    Serial.print("FRONTSIG: ");
    Serial.println(digitalRead(FRONTSIG));
    Serial.print("LEFTSIG: ");
    Serial.println(digitalRead(LEFTSIG));
    Serial.print("RIGHTSIG: ");
    Serial.println(digitalRead(RIGHTSIG));
    Serial.print("REARSIG: ");
    Serial.println(digitalRead(REARSIG));
    Serial.print("ERRORSIG: ");
    Serial.println(digitalRead(ERRORSIG));
  #endif
  
}

//Updates given signal in case given distance is to short
unsigned char determine_blocked(unsigned char dist){
  return (dist <= MAX_DISTANCE);
}

