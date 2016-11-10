# define NUM_SOLENOIDS 6

#include <avr/interrupt.h>
#include <avr/io.h>

#define LED_POWER 13
#define LED_STATUS 12
#define arduinoID 2

char bytes[2];
short notes[NUM_SOLENOIDS];

int handshake = 0;
int statustimer = 0;

// actuator pins
int actuators[] = {
  3, 5, 6, 9, 10, 11
};

void setup() {
  Serial.begin(57600);

  // interrupt timer parameters
  TCCR2A = 1;
  TCCR2B = 3;
  TIMSK2 = 1;

  pinMode(LED_POWER, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  digitalWrite(LED_POWER, LOW);

  for (int i = 0; i < NUM_SOLENOIDS; i++) {
    pinMode(actuators[i], OUTPUT);
    digitalWrite(actuators[i], LOW);
  }
}

ISR(TIMER2_OVF_vect) {
  // solenoid control
  for (int i = 0; i < NUM_SOLENOIDS; i++) {
    if (notes[i] > 0) {
      digitalWrite(actuators[i], HIGH);
      notes[i]--;
    }
    else {
      digitalWrite(actuators[i], LOW);
    }
  }
  if (statustimer > 0) {
    digitalWrite(LED_STATUS, HIGH);
    statustimer--;
  }
  else {
    digitalWrite(LED_STATUS, LOW);
  }
}

void loop() {
  if (Serial.available()) {
    if (Serial.read() == 0xff) {
      // reads in a two index array from ChucK
      Serial.readBytes(bytes, 2);

      // bit wise operations
      // ~~~~~~~~~~~~~~~~~~~
      // reads the first six bits for the note number
      // then reads the last ten bits for the note velocity
      int pitch = byte(bytes[0]) >> 2;
      int velocity = (byte(bytes[0]) << 8 | byte(bytes[1])) & 1023;

      // message required for "handshake" to occur
      // happens once per Arduino at the start of the ChucK serial code
      if (pitch == 63 && velocity == 1023 && handshake == 0) {
        Serial.write(arduinoID);
        handshake = 1;
      }
      
      if (pitch >= 0 && pitch <= NUM_SOLENOIDS) {
        statustimer = 120;
        notes[pitch] = (velocity * 1.0);
      }
    }
  }
}
