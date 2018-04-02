#define In1 3
#define In2 2
#define enA 9 //Enable pins for Motor1

#define In3 7
#define In4 8
#define enB 5  //Enable pins for Motor2

#define DriveBit1 10
#define DriveBit2 11
#define DriveBit3 13  //Pins used by RPI to controll the engines


void setup() {
  Serial.begin(9600);
  
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT); 
  pinMode(enA, OUTPUT); // Set pins to output Motor1
  
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(enB, OUTPUT); //Set pins to output Motor2

  pinMode(DriveBit1, INPUT); //Inputs from RPI
  pinMode(DriveBit2, INPUT);
  pinMode(DriveBit3, INPUT);
}

//
unsigned char LeftSpeed=0;
unsigned char RightSpeed=0;
unsigned char readDriveBit1;
unsigned char readDriveBit2;
unsigned char readDriveBit3;
unsigned char state=0;

void loop() {
  readDriveBit1 = digitalRead(DriveBit1);
  readDriveBit2 = digitalRead(DriveBit2);
  readDriveBit3 = digitalRead(DriveBit3);
 // readDriveBit1 = 1;
 // readDriveBit2 = 0;
 // readDriveBit3 = 0;
  
  //Stupid shift thing
  unsigned char dir =0;
  dir = dir | (unsigned char)readDriveBit1;
  dir = dir | ((unsigned char)readDriveBit2 <<1);
  dir = dir | ((unsigned char)readDriveBit3 <<2);

  changeEngines(dir);

  //Write the speed to the engine
  analogWrite(enA, RightSpeed);
  analogWrite(enB, LeftSpeed);
}

void changeEngines(unsigned char dir){
  if(dir == 0b00000000){
      //Stop
      forwardsRightEngine();
      forwardsLeftEngine();
      LeftSpeed=0;
      RightSpeed=0;
     
      if(state != 0){
        delayEngine();
      }
      state =0;

    }else if(dir == 0b00000001){
      //Forward
      forwardsRightEngine();
      forwardsLeftEngine();
      LeftSpeed=150;
      RightSpeed=140;
      
      if(state != 1){
        delayEngine();
      }
      state =1;
      
    }else if(dir == 0b00000010){
      //Backwards
      backwardsRightEngine();
      backwardsLeftEngine();
      LeftSpeed=150;
      RightSpeed=140;

      if(state != 2){
        delayEngine();
      }
      state =2;
      
    }else if(dir == 0b00000011){
      //Right
      backwardsRightEngine();
      forwardsLeftEngine();
      LeftSpeed=100;
      RightSpeed=90;

      if(state != 3){
        delayEngine();
      }
      state =3;
      
      
    }else if(dir == 0b00000100){
      //Left
      forwardsRightEngine();
      backwardsLeftEngine();
      LeftSpeed=100;
      RightSpeed=90;


      if(state != 4){
        delayEngine();
      }
      state =4;
      
    }else if(dir == 0b00000101){
    }else if(dir == 0b00000110){
    }else if(dir == 0b00000111){
    }else{
    }
  }
  /*
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
    LeftSpeed = 160;
    RightSpeed = 150;
   }
  }
*/
void forwardsLeftEngine(){
   //Forwards settings for left engine
    digitalWrite(In1,LOW);
    digitalWrite(In2,HIGH);
}
void forwardsRightEngine(){
   //Forwards settings for right engine
    digitalWrite(In3,LOW);
    digitalWrite(In4,HIGH);
    }
void backwardsLeftEngine(){
    //Backwards settings for left engine
    digitalWrite(In1,HIGH);
    digitalWrite(In2,LOW);
    }
void backwardsRightEngine(){
   //Backwards settings for right engine
    digitalWrite(In3,HIGH);
    digitalWrite(In4,LOW);
    }

void delayEngine(){
  //This is so that the engine gets some time to rev-down
  analogWrite(enA, 0);
  analogWrite(enB, 0);
  delay(200);
  }

