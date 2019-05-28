#include "serialInterface.h"

#include "Arduino.h"

void SerialInterface::send(const char* string) {
  Serial.print(string);
}

void SerialInterface::send(const Command& command) {
  Serial.print(command.getName());
  Serial.print(" ");
  Serial.print(command.getBody());
}

void SerialInterface::sendLine(const char* string) {
  Serial.println(string);
}

void SerialInterface::sendLine(const Command& command) {
  Serial.print(command.getName());
  Serial.print(" ");
  Serial.println(command.getBody());
}

void SerialInterface::read() {
  int count = 0;
  // Read bytes until there are no more to read
  for (int byte = Serial.read(); byte != -1; byte = Serial.read()) {
    char c = (char) byte;
    add(c == '\n' ? '\0' : c);
    count++;
  }

  if (count > 0) {
    Serial.print("Read ");
    Serial.println(count);
  }

  // Process any lines that have appeared
  bool nullTerminatorFound = false;
  int startOfString = 0;
  for (int i = 0; i < bufferIndex; i++) {
    if (buffer[i] == '\0') {
      handleLine(&buffer[startOfString]);
      nullTerminatorFound = true;
      startOfString = i + 1;
    }
  }

  // Copy all characters to the front of the buffer
  if (nullTerminatorFound) {
    for (int i = 0; i + startOfString < bufferIndex; i++) {
      buffer[i] = buffer[i + startOfString];
    }

    // Reset the end pointer
    bufferIndex = bufferIndex - startOfString;
  }
}

void SerialInterface::handleLine(const char* line) {
  send("Input: ");
  sendLine(line);
}

void SerialInterface::print() {
  add('\0');
  sendLine("Printing");
  sendLine(&buffer[0]);
}

void SerialInterface::add(char character) {
  buffer[bufferIndex] = character;
  bufferIndex += 1;
}
