const int phase1pin = 2;
const int phase2pin = 3;
const int phase3pin = 4;
float holdTime = 500000; // microsecs
const unsigned long minHoldTime = 1300;
 
unsigned long p1start,
              p1end,
              p2start,
              p2end,
              p3start,
              p3end;
 
void setup(){
  Serial.begin(9600);
  pinMode(phase1pin, OUTPUT);
  pinMode(phase2pin, OUTPUT);
  pinMode(phase3pin, OUTPUT);
  p1start = micros();
  digitalWrite(phase1pin, HIGH);
}
 
 
void chkP1(){
  unsigned long currentTime = micros();
  unsigned long td = currentTime - p1start;
  unsigned long refractory = 2.25*holdTime;
  if(digitalRead(phase1pin)){
    if(td > holdTime){
      digitalWrite(phase1pin, LOW);
      p1end = currentTime;
    }
  }else if(td > refractory){
    digitalWrite(phase1pin, HIGH);
    p1start = currentTime;
  }
}
 
void chkP2(){
  unsigned long currentTime = micros();
  unsigned long td = currentTime - p1start;
  if(digitalRead(phase2pin)){
    if(td > 1.75*holdTime || td < 0.75*holdTime){
      digitalWrite(phase2pin, LOW);
      p2end = currentTime;
    }
  }else if(td > 0.75*holdTime && td < 1.75*holdTime){
    digitalWrite(phase2pin, HIGH);
    p2start = currentTime;
  }
}
 
void chkP3(){
  unsigned long currentTime = micros();
  unsigned long td = currentTime - p1start;
  if(digitalRead(phase3pin)){
    if(td > 0.25*holdTime && p3start < p1start){
      digitalWrite(phase3pin, LOW);
      p3end = currentTime;
    }
  }else if(td > 1.5*holdTime){
    digitalWrite(phase3pin, HIGH);
    p3start = currentTime;
  }
}
 
void loop(){
  chkP1();
  chkP2();
  chkP3();
  delayMicroseconds(100);
  if(holdTime >= minHoldTime){
    holdTime -= 0.5;
  }
}
