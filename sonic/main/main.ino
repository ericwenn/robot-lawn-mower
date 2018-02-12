#include <Ultrasonic.h>


#define MIN_DISTANCE 25
#define FRONT_OFFSET 0
#define LEFT_OFFSET 0
#define RIGHT_OFFSET 0
#define REAR_OFFSET 0

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

unsigned char signals;


void setup() {
  pinMode(LEFTSIG, OUTPUT); //LEFTSIG
  pinMode(FRONTSIG, OUTPUT); //FRONTSIG
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
  unsigned char _frontFront = frontFront.distanceRead();

  //Check on the left and right side on the front
  unsigned char _frontLeft = frontLeft.distanceRead();
  unsigned char _frontRight = frontRight.distanceRead();

  //De-bug
/*
  Serial.print(" Dist FrontRight: ");
  Serial.print(frontRight.distanceRead());

  Serial.print(" Dist Front: ");
  Serial.print(frontFront.distanceRead());

  Serial.print(" Dist FrontLeft: ");
  Serial.println(frontLeft.distanceRead());
  */

  Serial.print("FrontLeft ");
  Serial.print(_frontLeft);
  Serial.print(" ");
  Serial.print(determine_blocked(_frontLeft));
  //digitalWrite(LEFTSIG,LOW); // can be better looking

  Serial.print(" FrontFront ");
  Serial.print(_frontFront);
  Serial.print(" ");
  Serial.print(determine_blocked(_frontFront));
  //FRONTSIG = determine_blocked(_frontFront); // can be better looking

  Serial.print(" FrontRight ");
  Serial.print(_frontRight);
  Serial.print(" ");
  Serial.println(determine_blocked(_frontRight));
 // RIGHTSIG = determine_blocked(_frontRight); // can be better looking
  
  return c;
  
}


unsigned char determine_blocked(char dist){
  //unsigned char dist = sensor.distanceRead();
  //if 0, means its too far away for the sensors
  if(dist <= MIN_DISTANCE && dist != 0){
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

