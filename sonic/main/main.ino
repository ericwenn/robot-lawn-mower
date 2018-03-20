#include <SoftwareSerial.h>
#include <Ultrasonic.h>
#define DEBUG

#define MAX_DISTANCE 25

#define LEFTSIG 14
#define FRONTSIG 15
#define RIGHTSIG 16

#define TRIG_RIGHT 10
#define TRIG_FRONT 11
#define TRIG_LEFT 12

#define ECHO_RIGHT 7
#define ECHO_FRONT 8
#define ECHO_LEFT 9

#define TIMEOUT 40000UL

//Sensor declarations
Ultrasonic sonicRight(TRIG_RIGHT,ECHO_RIGHT, TIMEOUT);
Ultrasonic sonicFront(TRIG_FRONT,ECHO_FRONT,TIMEOUT);
Ultrasonic sonicLeft(TRIG_LEFT,ECHO_LEFT, TIMEOUT);

SoftwareSerial serialRPi (15,16);

void setup() {
  pinMode(LEFTSIG, OUTPUT); //LEFTSIG
  pinMode(FRONTSIG, OUTPUT); //FRONTSIG
  pinMode(RIGHTSIG, OUTPUT); //RIGHTSIG

  serialRPi.begin(9600);

  #ifdef DEBUG
    Serial.begin(9600);
  #endif
}

void loop() {
  check_sensors();
}

void check_sensors(){
  
  //Read sensors and trigger relevant signal pin if blocked
  //LEFT
  unsigned char _sonicLeft = sonicLeft.distanceRead();
  delay(6);
  unsigned char blockedLeft = determine_blocked(_sonicLeft);
  digitalWrite(LEFTSIG, blockedLeft);
  
  //FRONT
  unsigned char _sonicFront = sonicFront.distanceRead();
  delay(6);
  unsigned char blockedFront = determine_blocked(_sonicFront);
  digitalWrite(FRONTSIG,blockedFront);
 
  //RIGHT
  unsigned char _sonicRight = sonicRight.distanceRead();
  delay(6);
  unsigned char blockedRight = determine_blocked(_sonicRight);
  digitalWrite(RIGHTSIG,blockedRight);

  char serialValues[] = {blockedLeft,blockedFront,blockedRight};
  serialRPi.write(serialValues);

  #ifdef DEBUG
    //If you use a smart serial monitor (like putty) these two lines will do you good
    //Serial.print("\033[2j");
    //Serial.print("\033[H");
    
    Serial.print("Left ");
    Serial.print(_sonicLeft);
    Serial.print(" ");
    Serial.println(determine_blocked(_sonicLeft));
  
    Serial.print("Front ");
    Serial.print(_sonicFront);
    Serial.print(" ");
    Serial.println(determine_blocked(_sonicFront));
  
    Serial.print("Right ");
    Serial.print(_sonicRight);
    Serial.print(" ");
    Serial.println(determine_blocked(_sonicRight));
    Serial.println("");

    /*Serial.print("FRONTSIG: ");
    Serial.println(digitalRead(FRONTSIG));
    Serial.print("LEFTSIG: ");
    Serial.println(digitalRead(LEFTSIG));
    Serial.print("RIGHTSIG: ");
    Serial.println(digitalRead(RIGHTSIG));
    */
  #endif
  
}

//Updates given signal in case given distance is to short
unsigned char determine_blocked(unsigned char dist){
  return (dist <= MAX_DISTANCE && dist !=0);
}

