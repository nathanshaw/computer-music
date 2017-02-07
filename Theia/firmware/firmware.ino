/*
Firware for the Theia SR-04 Ultrasonic Rangefinder control shield
 
 This firware handles up to eight Ultrasonics
 
 ---------- For each new bot--------------
 The Theia boards have ArduinoID's of between 51 and 60
 Change the define statement for ARDUINO_ID
 Change the define statement for NUM_RANGEFINDERS
 Change the LED_FEEDBACK define statement to 0 if you only want leds to
 be active when system is booting
 Change POLLING_DELAY to the number of MS you between each polling
 
 TODO:::
 
 - add some feedback for the LED?
 - setup slow interupt to trigger the ultrasonics every 50ms or so?
 - when message comes in for distance it just returns the most rescent result?

 */
#define LED_FEEDBACK 1
#define NUM_RANGEFINDERS 4
#define BOT_ID 2
#define BOARD_TYPE 4
#define ARDUINO_ID 1

#define RED_LED 12
#define GREEN_LED 13
#define POLLING_DELAY 50

// for interfacing with the the SR-04 rangefinders
const int trigPins[8] = {
  A4, A2, A0, 2, 8, 10, 4, 6};
const int echoPins[8] = {
  A5, A3, A1, 3, 9, 11, 5, 7};

// most current readings from the ultrasonics
uint8_t lastDistance[NUM_RANGEFINDERS];

int handshake = 0;
char bytes[2];

// Setup loop //
void setup() {
  Serial.begin (57600);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  // set the LED to yellow for setup loop
  digitalWrite(RED_LED, HIGH);
  digitalWrite(GREEN_LED, HIGH);
  for (int i; i < NUM_RANGEFINDERS; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
  }
  // give a second for things to settle and
  // to notice that the LED was turned on
}

// read all of the ultrasonics
void readUltrasonics() {
  if (LED_FEEDBACK) {
     digitalWrite(GREEN_LED, HIGH); 
  }
  for( int i; i < NUM_RANGEFINDERS; i++) {
    long duration;
    digitalWrite(trigPins[i], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPins[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPins[i], LOW);
    duration = pulseIn(echoPins[i], HIGH);
    lastDistance[i] = duration / 58.2;
  } 
  if (LED_FEEDBACK) {
     digitalWrite(GREEN_LED, LOW); 
  }
}

// read a specific ultrasonic 
void readUltrasonic(int which) {
  if (LED_FEEDBACK) {
     digitalWrite(GREEN_LED, HIGH); 
     digitalWrite(RED_LED, HIGH); 
  }
  if (which < NUM_RANGEFINDERS){  
    long duration;
    digitalWrite(trigPins[which], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPins[which], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPins[which], LOW);
    duration = pulseIn(echoPins[which], HIGH);
    // if it is farther away, we just take 253
    lastDistance[which] = min(0xFE, duration / 58.2);
  }
  if (LED_FEEDBACK) {
     digitalWrite(GREEN_LED, LOW);
     digitalWrite(RED_LED, LOW); 
  }
}

void sendDistances() {
  // parity byte
  Serial.print(char(0xFF));
  for (int i; i < 8; i++) {
    Serial.print(char(lastDistance[i]));
  }
}

void sendDistance(int which) {
  Serial.print(char(0xFF));
  Serial.print(char(lastDistance[which]));
}

void pollSerial() {
  if (Serial.available()) {
    if (Serial.read() == 0xff) {
      // reads in a two index array from ChucK

      Serial.readBytes(bytes, 2);
      // bit wise operations
      // ~~~~~~~~~~~~~~~~~~~
      // reads the first six bits for the note number
      // then reads the last ten bits for the note velocity
      int sensor = byte(bytes[0]) >> 2;
      int parity = (byte(bytes[0]) << 8 | byte(bytes[1])) & 1023;

      // message required for "handshake" to occur
      // happens once per Arduino at the start of the ChucK serial code
      if (sensor == 63 && parity == 1023 && handshake == 0) {
        Serial.write(BOT_ID);
        Serial.write(BOARD_TYPE);
        Serial.write(ARDUINO_ID);
        handshake = 1;
        digitalWrite(RED_LED, LOW);
        digitalWrite(GREEN_LED, LOW);
      }
      // if the sensor is between 1 and NUM_RANGEFINDERS
      // and the parity is 0x00 we return the range of
      // the rangefinder
      else if (sensor >= 0) {
          // the solinoids are addressed using index = 0
          readUltrasonic(sensor); 
          sendDistance(sensor);
      }
      else {
         sendDistance(254); 
      }
    }
  }  
}

void loop() {
  pollSerial();
}
