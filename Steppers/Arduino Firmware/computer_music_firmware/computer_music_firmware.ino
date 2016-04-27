/*
  Stepper Motor Control - For Ajays Motor

  This code is for the


*/
#include <Stepper.h>

// these moth
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution
int driveOpen[] = {false, false, false, false};
byte dataBytes[3];

// for your motor
Stepper myStepper1(stepsPerRevolution, 2, 3, 4, 5);
Stepper myStepper2(stepsPerRevolution, 6, 7, 8, 9);
Stepper myStepper3(stepsPerRevolution, 10, 11, 12, 13);
Stepper myStepper4(stepsPerRevolution, A0, A1, A2, A3);

void setup() {
  Serial.begin(57600);
  Serial.print("booted");
}

void handleMsg(byte channel, uint16_t velocity) {
  /*
     Takes in a drive number and a velocity
  */
  switch (channel) {
    case 1:
      myStepper1.setSpeed(velocity);
      if (!driveOpen[0]) {
        myStepper1.step(stepsPerRevolution);
        driveOpen[0] = true;
      }
      else {
        myStepper1.step(-stepsPerRevolution);
        driveOpen[0] = false;
      }
      break;

    case 2:
      myStepper2.setSpeed(velocity);
      if (!driveOpen[1]) {
        myStepper2.step(stepsPerRevolution);
        driveOpen[1] = true;
      }
      else {
        myStepper2.step(-stepsPerRevolution);
        driveOpen[1] = false;
      }
      break;

    case 3:
      myStepper3.setSpeed(velocity);
      if (!driveOpen[2]) {
        myStepper3.step(stepsPerRevolution);
        driveOpen[2] = true;
      }
      else {
        myStepper3.step(-stepsPerRevolution);
        driveOpen[2] = false;
      }
      break;

    case 4:
      myStepper4.setSpeed(velocity);
      if (!driveOpen[3]) {
        myStepper4.step(stepsPerRevolution);
        driveOpen[3] = true;
      }
      else {
        myStepper4.step(-stepsPerRevolution);
        driveOpen[3] = false;
      }
      break;
  }
}

void serialPoller() {
  while(Serial.available()) {
    if (Serial.available()) {
      Serial.readBytes((char*)dataBytes, 3);
      /*
       * if (Serial.available() > 3) {
        Serial.flush();
      }
      */
      if (dataBytes[0] == 0xFF) {
        byte driveNum = dataBytes[1];
        uint16_t velocity = dataBytes[2]*2;
        handleMsg(driveNum, velocity);
        
      }
    }
    else {
      Serial.flush();
    }
  }
}

void loop() {
  serialPoller();
}
