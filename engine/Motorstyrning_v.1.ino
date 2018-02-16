#define In1 12
#define In2 4
#define enA 9 //Enable pins for Motor1

#define In3 7
#define In4 8
#define enB 5  //Enable pins for Motor2

void setup() {
  Serial.begin(9600);
  
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT); 
  pinMode(enA, OUTPUT); // Set pins to output Motor1
  
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(enB, OUTPUT); //Set pins to output Motor2
  
}
void goStraightForward(){
  digitalWrite(In1,HIGH);
  digitalWrite(In2,LOW);
  
  digitalWrite(In3,HIGH);
  digitalWrite(In4,LOW);

  Serial.print(enB);
  
  analogWrite(enA,255);
  analogWrite(enB,255);
}
void goBackwards(){
  digitalWrite(In1,LOW);
  digitalWrite(In2,HIGH);

  digitalWrite(In3,LOW);
  digitalWrite(In4,HIGH);
  
  analogWrite(enA,150);
  analogWrite(enB,150);
}
void goLeft(){
  digitalWrite(In1,LOW);
  digitalWrite(In2,HIGH);

  digitalWrite(In3,HIGH);
  digitalWrite(In4,LOW);
  
  analogWrite(enA,50);
  analogWrite(enB,150);
}
void goRight(){
  
  digitalWrite(In1,HIGH);
  digitalWrite(In2,LOW); 

  digitalWrite(In3,HIGH);
  digitalWrite(In4,LOW);
  
  analogWrite(enA,150);
  analogWrite(enB,50);
}

void loop() {
  goStraightForward();
}
