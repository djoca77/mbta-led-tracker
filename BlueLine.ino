int latchPin = 8;
int clockPin = 12;
int dataPin = 11;

int blueStops = 12
int redStops = 22
int orangeStops = 16

void setup() {
  pinMode(latchPin, OUTPUT); //latch to control shift register pins
  pinMode(clockPin, OUTPUT); //clock for shift register to read in bits one by one
  pinMode(dataPin, OUTPUT); //data
  Serial.begin(9600);
}

void sendBits(String bits) {
    // Parse the 12-bit string into two bytes
  byte highByte = 0; // Bits 0-7
  byte lowByte = 0;  // Bits 8-11

  for (int i = 0; i < blueStops; i++){
    if (bitString[i] == '1') {
      if (i < 8) {
        highByte |= (1 << (7 - i)); // Set bit in highByte
      } else {
        lowByte |= (1 << (11 - i)); // Set bit in lowByte
      }
    }
  }

  digitalWrite(latchPin, LOW);
  shiftout(dataPin, clockPin, LSBFIRST, highByte);
  shiftout(dataPin, clockPin, LSBFIRST, lowByte)
  digitalWrite(latchPin, HIGH);
  delay(1000);

}

void loop() {
  if (Serial.available() > 0) {
    String str = Serial.readString();
    sendBits(str);
  }
}


