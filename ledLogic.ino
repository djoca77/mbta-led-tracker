int latchPin1 = 8;
int latchPin2 = 7;
int latchPin3 = 6;

int clockPin = 12;

int bluePin = 11;
int orangePin = 10;
int redPin = 9;

int blueStops = 12;
int redStops = 22;
int orangeStops = 20;
int greenStops = 72;

 void setup() {
  pinMode(latchPin1, OUTPUT);  //latch to control shift register pins for blue line
  pinMode(latchPin2, OUTPUT);  //latch to control shift register pins for orange line
  pinMode(latchPin3, OUTPUT);   //latch to control shift register pins for red line
  pinMode(clockPin, OUTPUT);  //clock for shift register to read in bits one by one
  pinMode(bluePin, OUTPUT);   //blue data
  pinMode(orangePin, OUTPUT); //orange data
  pinMode(redPin, OUTPUT);    //red data

  Serial.begin(9600);
}

void sendBlue(String bits) {
  // Parse the 12-bit string into two bytes
  byte highByte = 0;  // Bits 0-7
  byte lowByte = 0;   // Bits 8-11

  for (int i = 0; i < blueStops; i++) {
    if (bits[i] == '1') {
      if (i < 8) {
        highByte |= (1 << (7 - i));  // Set bit in highByte
      } else {
        lowByte |= (1 << (11 - i));  // Set bit in lowByte
      }
    }
  }
  digitalWrite(latchPin1, LOW);

  shiftOut(bluePin, clockPin, LSBFIRST, lowByte);
  shiftOut(bluePin, clockPin, LSBFIRST, highByte);

  digitalWrite(latchPin1, HIGH);
}

void sendOrange(String bits) {
  // Parse the 20-bit string into three bytes
  byte highByte = 0;  // Bits 0-7
  byte midByte = 0;   // Bits 8-15
  byte lowByte = 0;   // Bits 16-19

  for (int i = 0; i < orangeStops; i++) {
    if (bits[i] == '1') {
      if (i < 8) {
        highByte |= (1 << (7 - i));  // Set bit in highByte
      } else if (i >= 8 && i < 16 ) {
        midByte |= (1 << (15 - i));  // Set bit in lowByte
      } else {
        lowByte |= (1 << (19 - i));  // Set bit in lowByte
      }
    }
  }
  digitalWrite(latchPin2, LOW);

  shiftOut(orangePin, clockPin, LSBFIRST, lowByte);
  shiftOut(orangePin, clockPin, LSBFIRST, midByte);
  shiftOut(orangePin, clockPin, LSBFIRST, highByte);

  digitalWrite(latchPin2, HIGH);
}

void sendRed(String bits) {
  // Parse the 22-bit string into three bytes
  byte highByte = 0;  // Bits 0-7
  byte midByte = 0;   // Bits 8-15
  byte lowByte = 0;   // Bits 16-21

  for (int i = 0; i < orangeStops; i++) {
    if (bits[i] == '1') {
      if (i < 8) {
        highByte |= (1 << (7 - i));  // Set bit in highByte
      } else if (i >= 8 && i < 16 ) {
        midByte |= (1 << (15 - i));  // Set bit in midByte
      } else {
        lowByte |= (1 << (21 - i));  // Set bit in lowByte
      }
    }
  }
  digitalWrite(latchPin3, LOW);

  shiftOut(redPin, clockPin, LSBFIRST, lowByte);
  shiftOut(redPin, clockPin, LSBFIRST, midByte);
  shiftOut(redPin, clockPin, LSBFIRST, highByte);

  digitalWrite(latchPin3, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String str = Serial.readString();
    if (str.substring(0,1) == "b") {
      sendBlue(str.substring(1));
    } else if (str.substring(0,1) == "o") {
      sendOrange(str.substring(1));
    } else if (str.substring(0,1) == "r") {
      sendRed(str.substring((1)));
    }
  }
}
