uint8_t portaState = 0xF0;

void setup() {
  // put your setup code here, to run once:
  DDRA = 0xFF;
  PORTA = 0x00;
  PORTB = 0xff;
  PORTC = 0xff;
  PORTL = 0xff;
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  PORTA = random(255);
  delay(200);
  PORTA = random(255);
}
