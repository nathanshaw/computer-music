
/*
  Stepper Motor Control - For Ajays Motor

  This code is for the


*/

#include <Stepper.h>
#include <MIDI.h>

MIDI_CREATE_DEFAULT_INSTANCE();
// these moth
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution
int driveOpen[] = {false, false, false, false};

// for your motor
Stepper myStepper1(stepsPerRevolution, 2, 3, 4, 5);
Stepper myStepper2(stepsPerRevolution, 6, 7, 8, 9);
Stepper myStepper3(stepsPerRevolution, 10, 11, 12, 13);
Stepper myStepper4(stepsPerRevolution, A0, A1, A2, A3);

void setup() {
  // initialize the serial port:
  MIDI.setHandleNoteOn(handleNoteOn);
  MIDI.setHandleNoteOff(handleNoteOff);
  MIDI.begin(MIDI_CHANNEL_OMNI);
  Serial.begin(115200);
  Serial.print("booted");
}

void handleNoteOff(byte channel, byte pitch, byte velocity) {
  
  Serial.print(channel);
  Serial.print(" - ");
  Serial.print(pitch);
  Serial.print(" - ");
  Serial.println(velocity);
  
  switch (channel) {

    case 1:
      myStepper1.setSpeed(pitch);
      if (driveOpen[0]) {
        myStepper1.step(-stepsPerRevolution);
        driveOpen[0] = false;
      }
      break;

    case 2:
      myStepper2.setSpeed(pitch);
      if (driveOpen[1]) {
        myStepper2.step(-stepsPerRevolution);
        driveOpen[1] = false;
      }
      break;

    case 3:
      myStepper3.setSpeed(pitch);
      if (driveOpen[2]) {
        myStepper3.step(-stepsPerRevolution);
        driveOpen[2] = false;
      }
      break;

    case 4:
      myStepper4.setSpeed(pitch);
      if (driveOpen[3]) {
        myStepper4.step(-stepsPerRevolution);
        driveOpen[3] = false;
      }
      break;
  }
}

void handleNoteOn(byte channel, byte pitch, byte velocity) {
  /*
     Takes in a drive number and a velocity
  */
    Serial.print(channel);
  Serial.print(" - ");
  Serial.print(pitch);
  Serial.print(" - ");
  Serial.println(velocity);
  switch (channel) {

    case 1:
      myStepper1.setSpeed(velocity);
      if (!driveOpen[0]) {
        myStepper1.step(stepsPerRevolution);
        driveOpen[0] = true;
      }
      break;

    case 2:
      myStepper2.setSpeed(velocity);
      if (!driveOpen[1]) {
        myStepper2.step(stepsPerRevolution);
        driveOpen[1] = true;
      }
      break;

    case 3:
      myStepper3.setSpeed(velocity);
      if (!driveOpen[2]) {
        myStepper3.step(stepsPerRevolution);
        driveOpen[2] = true;
      }
      break;

    case 4:
      myStepper4.setSpeed(velocity);
      if (!driveOpen[3]) {
        myStepper4.step(stepsPerRevolution);
        driveOpen[3] = true;
      }
      break;
  }
}

void loop() {
  MIDI.read();
}
