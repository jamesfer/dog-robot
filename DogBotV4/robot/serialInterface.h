#pragma once

#include "command.h"

class SerialInterface {
private:
  char buffer[512];
  unsigned int bufferIndex = 0;

public:
  void send(const char* string);
  void send(const Command& command);

  void sendLine(const char* line);
  void sendLine(const Command& command);

  void read();

  void handleLine(const char* line);

  void print();

private:
  void add(char character);
};
