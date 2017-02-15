/*
Stepper Motor Control - For Ajays Motor
 This code is for the HDD drives (to pull the strings)
 */
#include <Stepper.h>
#include <avr/interrupt.h>
#include <avr/io.h>

// for the handshake
const uint8_t ID = 21;

//its actually 100, but one revolution is too much
const int stepsPerRevolution = 100;  // change this to fit the number of steps per revolution
int driveOpen[] = {
  false, false, false, false};

char dataBytes[3];
byte stepsTaken[4] = {
  0,0,0,0};

int stepperSpeed[4] = {
  30, 30, 30, 30};

const uint16_t downSpeed = 200;
const uint8_t compThresh[4] = {
  6, 15, 15, 15};
const float turnScale = 0.55;
// Leds
const uint8_t red_led_pin = A5;
const uint8_t green_led_pin = A4;
int handshake = 0;
boolean green_led_state;
boolean red_led_state;
int stepsNeeded[4] = {200, 200, 200, 200};

// for your motor
Stepper myStepper1(stepsPerRevolution, 2, 3, 4, 5);
Stepper myStepper2(stepsPerRevolution, 6, 7, 8, 9);
Stepper myStepper3(stepsPerRevolution, 10, 11, 12, 13);
Stepper myStepper4(stepsPerRevolution, A0, A1, A2, A3);

void setup() {
  myStepper1.setSpeed(55);
  myStepper2.setSpeed(155);
  myStepper3.setSpeed(35);
  myStepper4.setSpeed(85);
  pinMode(red_led_pin, OUTPUT);
  pinMode(green_led_pin, OUTPUT);
  digitalWrite(red_led_pin, HIGH);
  digitalWrite(green_led_pin, HIGH);
  // interrupt timer parameters
  TCCR2A = 1;
  TCCR2B = 3;
  // enable the overflow interupt 
  TIMSK2 = 1;
  //
  delay(1000);
  Serial.begin(57600);
}

ISR(TIMER2_OVF_vect) {
  // solenoid control
  /*
   if (stepsNeeded[0] > 0) {
   myStepper1.step(1);      
   stepsNeeded[0]--;
   }
   if (stepsNeeded[1] > 0) {
   myStepper2.step(1);      
   stepsNeeded[1]--;
   }
   if (stepsNeeded[2] > 0) {
   myStepper3.step(1);      
   stepsNeeded[2]--;
   }
   if (stepsNeeded[3] > 0) {
   myStepper4.step(1);      
   stepsNeeded[3]--;
   }
   */
}

void spinSpinners() {
  red_led_state = !red_led_state;
  //digitalWrite(red_led_pin, red_led_state);
  if (stepsNeeded[0] > 0) {
    myStepper1.step(1);      
    stepsNeeded[0]--;
    green_led_state = !green_led_state;
    //digitalWrite(green_led_pin, green_led_state);
  }
  if (stepsNeeded[1] > 0) {
    myStepper2.step(1);      
    stepsNeeded[1]--;
  }
  if (stepsNeeded[2] > 0) {
    myStepper3.step(1);      
    stepsNeeded[2]--;
  }
  if (stepsNeeded[3] > 0) {
    myStepper4.step(1);      
    stepsNeeded[3]--;
  } 
}

void loop() {
  if (Serial.available()) {
    //spinSpinners();
    if (Serial.read() == 0xff) {
      // reads in a two index array from ChucK
      Serial.readBytes(dataBytes, 2);
      // bit wise operations
      // ~~~~~~~~~~~~~~~~~~~
      // reads the first six bits for the note number
      // then reads the last ten bits for the note velocity
      int pitch = byte(dataBytes[0]) >> 2;
      int velocity = (byte(dataBytes[0]) << 8 | byte(dataBytes[1])) & 1023;
      // message required for "handshake" to occur
      // happens once per Arduino at the start of the ChucK serial code
      if (pitch == 63 && velocity == 1023 && handshake == 0) {
        Serial.write(ID);
        handshake = 1;
      }
      if (pitch >= 0 && pitch <= 4) {
        red_led_state = !red_led_state;
        // digitalWrite(red_led_pin, red_led_state);
        // handleMsg(pitch, velocity);
        stepsNeeded[pitch] = stepsNeeded[pitch] + int(velocity/5);
        if (pitch == 0) {
           myStepper1.setSpeed(max(35, velocity*3)); 
        }
        else if (pitch == 1) {
           myStepper2.setSpeed(max(35, velocity*3)); 
        }
        else if (pitch == 2) {
           myStepper3.setSpeed(max(35, velocity*3)); 
        }
        else if (pitch == 3) {
           myStepper4.setSpeed(max(35, velocity*3)); 
        }

        }
      }
    }
  spinSpinners();
}


