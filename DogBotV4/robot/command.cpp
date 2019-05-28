#include "command.h"

Command::Command(const char* name, const char* body): name(name), body(body) {}

const char* Command::getName() {
  return name;
}

const char* Command::getBody() {
  return body;
}
