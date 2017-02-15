/*
Stepper Motor Control - For Ajays Motor
This code is for the HDD drives (to pull the strings)
*/
#include <Stepper.h>

// for the handshake
const uint8_t id = 22;

//its actually 100, but one revolution is too much
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution
int driveOpen[] = {false, false, false, false};
byte dataBytes[3];
byte stepsTaken[4] = {0,0,0,0};
const uint16_t downSpeed = 200;
const uint8_t compThresh[4] = {6, 15, 15, 15};
const float turnScale = 0.55;
// Leds
const uint8_t red_led_pin = A4;
const uint8_t green_led_pin = A5;


// for your motor
Stepper myStepper1(stepsPerRevolution, 2, 3, 4, 5);
Stepper myStepper2(stepsPerRevolution, 6, 7, 8, 9);
Stepper myStepper3(stepsPerRevolution, 10, 11, 12, 13);
Stepper myStepper4(stepsPerRevolution, A0, A1, A2, A3);

void setup() {
  pinMode(red_led_pin, OUTPUT);
  pinMode(green_led_pin, OUTPUT);
  digitalWrite(red_led_pin, HIGH);
  digitalWrite(green_led_pin, LOW);
  delay(1000);
  Serial.begin(57600);
  Serial.print("booted");
  myStepper1.setSpeed(95);
  myStepper2.setSpeed(95);
  myStepper3.setSpeed(95);
  myStepper4.setSpeed(95);
  myStepper1.step(100);
  myStepper1.step(-100);
  myStepper2.step(100);
  myStepper2.step(-100);
  myStepper3.step(100);
  myStepper3.step(-100);
  myStepper4.step(100);
  myStepper4.step(-100);
  digitalWrite(red_led_pin, LOW);
  // digitalWrite(green_led_pin, HIGH);
}

void handleMsg(byte channel, uint16_t velocity) {
  /*
     Takes in a drive number and a velocity
  */
  switch (channel) {
    case 1:
      myStepper1.setSpeed(velocity);
      if (!driveOpen[0]) {
        myStepper1.step(-stepsPerRevolution*turnScale);
        driveOpen[0] = true;
                if (velocity > 50) {stepsTaken[0]++;};
        if(stepsTaken[0] > compThresh[0]) {
          stepsTaken[0] = 0;
          myStepper1.step(2);
        }
      }
      else {
        myStepper1.setSpeed(downSpeed*0.75);
        myStepper1.step(stepsPerRevolution*turnScale);
        driveOpen[0] = false;
      }
      break;

    case 2:
      myStepper2.setSpeed(velocity);
      if (!driveOpen[1]) {
        myStepper2.step(-stepsPerRevolution*turnScale);
        driveOpen[1] = true;
        if (velocity > 50) {stepsTaken[1]++;};
        
        if(stepsTaken[1] > compThresh[1]) {
          stepsTaken[1] = 0;
          myStepper2.step(2);
        }
      }
      else {
        myStepper2.setSpeed(downSpeed);
        myStepper2.step(stepsPerRevolution*turnScale);
        driveOpen[1] = false;
      }
      break;

    case 3:
      // for some reason this stepper is switched
      myStepper3.setSpeed(velocity);
      if (!driveOpen[2]) {
        myStepper3.step(stepsPerRevolution*turnScale);
        driveOpen[2] = true;
        
        if (velocity > 50) {stepsTaken[2]++;};
        if(stepsTaken[2] > compThresh[2]) {
          stepsTaken[2] = 0;
          myStepper3.step(2);
        }
      }
      else {
        myStepper3.setSpeed(downSpeed);
        myStepper3.step(-stepsPerRevolution*turnScale);
        driveOpen[2] = false;
      }
      break;

    case 4:
      myStepper4.setSpeed(velocity);
      if (!driveOpen[3]) {
        myStepper4.step(stepsPerRevolution*turnScale);
        driveOpen[3] = true;
        
        if (velocity > 50) {stepsTaken[3]++;};
        if(stepsTaken[3] > compThresh[3]) {
          stepsTaken[3] = 0;
          myStepper4.step(2);
        }
      }
      else {
        myStepper4.setSpeed(downSpeed);
        myStepper4.step(-stepsPerRevolution*turnScale);
        driveOpen[3] = false;
      }
      break;
  }    
}

void serialPoller() {
  while(Serial.available()) {
    if (Serial.available() > 2) {
      Serial.readBytes((char*)dataBytes, 3);
      if (dataBytes[0] == 0xFF) {
        if (dataBytes[1] == 0xFF) {
          Serial.write(id);
        }
        byte driveNum = dataBytes[1];
        uint16_t velocity = max(dataBytes[2], 35);
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
