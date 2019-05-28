#include "Arduino.h"
#include "serialInterface.h"

#define SERIAL_BAUD 115200

SerialInterface serialInterface;

void setup() {
  // Serial.begin has to be called in the main file. Not sure why.
  Serial.begin(SERIAL_BAUD);
}

//int count = 0;

void loop() {
//  if (count == 1000) {
//    serialInterface.print();
//  } else if (count > 1000) {
//    delay(100000000);
//    return;
//  }

  serialInterface.read();
  delay(1);
//  count += 1;
}
