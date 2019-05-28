#pragma once

class Command {
private:
  const char* name;
  const char* body;

public:
  Command(const char* name, const char* body);

  const char* getName();

  const char* getBody();
};
