#define In1 3
#define In2 2
#define enA 9 //Enable pins for Motor1

#define In3 7
#define In4 8
#define enB 5  //Enable pins for Motor2

#define LEFT 10
#define RIGHT 11
#define REVERSE 12  //Pins used by RPI to controll the engines


void setup() {
  Serial.begin(9600);
  
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT); 
  pinMode(enA, OUTPUT); // Set pins to output Motor1
  
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(enB, OUTPUT); //Set pins to output Motor2

  pinMode(LEFT, INPUT); //Inputs from RPI
  pinMode(RIGHT, INPUT);
  pinMode(REVERSE, INPUT);
  
  
}

//
unsigned char LeftSpeed=0;
unsigned char RightSpeed=0;
unsigned char LeftRead;
unsigned char RightRead;
unsigned char ReverseRead;

void loop() {
  //goStraightForward();
  /*LeftRead = digitalRead(LEFT);
  RightRead = digitalRead(RIGHT);
  ReverseRead = digitalRead(REVERSE);*/
  
  LeftRead = 0;
  RightRead = 0
  ReverseRead = 0;
  
  checkForwards();
  checkDirection();

  analogWrite(enA, LeftSpeed);
  analogWrite(enB, RightSpeed);
}

void checkForwards(){
  if(ReverseRead == 0){
    //Forwards settings for left engine
    digitalWrite(In1,HIGH);
    digitalWrite(In2,LOW);

    //Forwards settings for right engine
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    }else{
      //Backwards settings for left engine
      digitalWrite(In1,LOW);
      digitalWrite(In2,HIGH);
      //Backwards settings for right engine
      digitalWrite(In3,LOW);
      digitalWrite(In4,HIGH);
    }
  }
void checkDirection(){
  if(LeftRead == 0 && RightRead ==0){
    LeftSpeed = 0;
    RightSpeed = 0;
   }else if(LeftRead == 1 && RightRead ==0){
    LeftSpeed = 50;
    RightSpeed = 150;
   }else if(LeftRead == 0 && RightRead ==1){
    LeftSpeed = 150;
    RightSpeed = 50;
   }else if(LeftRead == 1 && RightRead ==1){
    LeftSpeed = 150;
    RightSpeed = 150;
   }

  }
void goStraightForward(){
  analogWrite(enA,255);
  analogWrite(enB,255);
}
void goBackwards(){
  analogWrite(enA,150);
  analogWrite(enB,150);
}
void goLeft(){
  analogWrite(enA,50);
  analogWrite(enB,150);
}
void goRight(){ 
  analogWrite(enA,150);
  analogWrite(enB,50);
}
