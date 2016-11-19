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

 */

#define RED_LED 12
#define GREEN_LED 13
#define LED_FEEDBACK 1
#define NUM_RANGEFINDERS 4
#define ARDUINO_ID 51
#define POLLING_DELAY 50

// for interfacing with the the SR-04 rangefinders
const int trigPins[8] = {
  A4, A2, A0, 2, 8, 10, 4, 6};
const int echoPins[8] = {
  A5, A3, A1, 3, 9, 11, 5, 7};

// most current readings from the ultrasonics
long lastDistance[NUM_RANGEFINDERS];

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
  delay(750);
  // turn the LED off
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void readUltraSonics() {
  for( int i; i < NUM_RANGEFINDERS; i++) {
    long duration;
    digitalWrite(trigPins[i], LOW);
    delayMicroseconds(2);
    digitalWrite(trigPins[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPins[i], LOW);
    duration = pulseIn(echoPins[i], HIGH);
    lastDistance[i] = (duration/2) / 29.1;
  } 
}

void sendDistances() {
  // parity byte
  Serial.print(0xFF);
  for (int i; i < 8; i++) {
    Serial.print(lastDistance[i]);
  }
}

void pollSerial() {
if (Serial.available()) {
    if (Serial.read() == 0xff) {
      // reads in a two index array from ChucK
      char bytes[2];
      Serial.readBytes(bytes, 2);
      // bit wise operations
      // ~~~~~~~~~~~~~~~~~~~
      // reads the first six bits for the note number
      // then reads the last ten bits for the note velocity
      int pitch = byte(bytes[0]) >> 2;
      int velocity = (byte(bytes[0]) << 8 | byte(bytes[1])) & 1023;

      // message required for "handshake" to occur
      // happens once per Arduino at the start of the ChucK serial code
      if (pitch == 63 && velocity == 1023) {
        Serial.write(ARDUINO_ID);
        handshake = 1;
      }
    }
  }  
}

void loop() {
  if (handshake != 1) {
    pollSerial(); 
  }
  readUltraSonics();
  sendDistances();
  delay(POLLING_DELAY);
}
