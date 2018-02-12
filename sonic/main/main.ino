#include <Ultrasonic.h>


#define MAX_DISTANCE 25
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
  //digitalWrite(FRONTSIG, LOW);
  signals = 0;

  //Used for debug
  Serial.begin(9600);
  Serial.println("Setup complete");
  
}

void loop() {
  signals = read_sensors(signals);
  //update_signals(signals);

}

unsigned char read_sensors(char c){
  
  //Check front for hit, if hit _front = 1 
  unsigned char _frontFront = frontFront.distanceRead();
  delay(4);
  //Check on the left and right side on the front
  unsigned char _frontLeft = frontLeft.distanceRead();
  delay(4);
  unsigned char _frontRight = frontRight.distanceRead();
  delay(4);
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
  
  if(determine_blocked(_frontLeft) == 1){ //can be better looking
    digitalWrite(LEFTSIG,HIGH);
    }else{
     digitalWrite(LEFTSIG,LOW); 
  }


  Serial.print(" FrontFront ");
  Serial.print(_frontFront);
  Serial.print(" ");
  Serial.print(determine_blocked(_frontFront));
  if(determine_blocked(_frontFront) == 1){ //can be better looking
    digitalWrite(FRONTSIG,HIGH);
    }else{
     digitalWrite(FRONTSIG,LOW); 
  }

  Serial.print(" FrontRight ");
  Serial.print(_frontRight);
  Serial.print(" ");
  Serial.println(determine_blocked(_frontRight));
  if(determine_blocked(_frontRight) == 1){ //can be better looking
    digitalWrite(RIGHTSIG,HIGH);
    }else{
     digitalWrite(RIGHTSIG,LOW); 
  }
  
  return c;
  
}


unsigned char determine_blocked(char dist){
  //unsigned char dist = sensor.distanceRead();
  //if 0, means its too far away for the sensors
  if(dist <= MAX_DISTANCE && dist > 0){
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

