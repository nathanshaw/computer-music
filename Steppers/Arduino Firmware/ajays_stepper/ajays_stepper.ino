
/*
  Stepper Motor Control - For Ajays Motor

  This code is for the 
  

*/

#include <Stepper.h>

#define CLOCK_WISE 1
#define COUNTER_CLOCK_WISE -1

// these moth
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(600);
  // initialize the serial port:
  Serial.begin(9600);
}

void sweepMotor(int from, int to, int factor, int dir) {
  if (from > to) {
    for (int i = from; i > to; i = i - factor) {
      myStepper.setSpeed(i);
      myStepper.step(stepsPerRevolution * dir);
    }
  }
  else {
    for (int i = from; i < to; i = i + factor) {
      myStepper.setSpeed(i);
      myStepper.step(stepsPerRevolution * dir);
    }
  }
}

void intro(int itters) {
  Serial.print("Intro : ");
  for (int i = 0; i < itters; i++) {
    Serial.print(i);
    sweepMotor(5000, 5100, 1, CLOCK_WISE);
    sweepMotor(8000, 4000, 15, COUNTER_CLOCK_WISE);
    sweepMotor(6000, 6200, 2, CLOCK_WISE);
    sweepMotor(9000, 6000, 22, COUNTER_CLOCK_WISE);
    myStepper.step(stepsPerRevolution * 100);
    Serial.print("-");
  }
  Serial.println(" ");
}

void chorus(int itters) {
  for (int i = 0; i < itters; i++) {
    /*
    myStepper.setSpeed(10000); // sonic warfare right here
    myStepper.step(stepsPerRevolution * 100);
    myStepper.setSpeed(8000);
    myStepper.step(stepsPerRevolution * 100);
    myStepper.setSpeed(random(30, 9000));
    myStepper.step(stepsPerRevolution * 100);
    */
    for (int ii = 10; ii < 2000; ii++) {
      myStepper.setSpeed(ii);
      Serial.println(ii);
    myStepper.step(stepsPerRevolution);  
    }
    
  }
}

void loop() {
  //intro(2);
  //chorus(100);
   myStepper.setSpeed(random(1000,15000));
   myStepper.step(stepsPerRevolution); 
}

