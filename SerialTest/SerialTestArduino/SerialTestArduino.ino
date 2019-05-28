//#define SERIAL_BAUD 9600
//#define SERIAL_BAUD 38400
//#define SERIAL_BAUD 57600
#define SERIAL_BAUD 115200

// Expected number of inputs
#define INPUT_COUNT 500

// Array of received input strings
char inputs[INPUT_COUNT][11];

// Current index in the inputs array
int inputIndex = 0;

// Current character index in the current input
int inputCharacterIndex = 0;

// Number of loops we have gone through
int loopCount = 0;

void receiveInput(char c) {
  if (c == '\n') {
    inputs[inputIndex][inputCharacterIndex] = '\0';
    inputCharacterIndex = 0;
    inputIndex += 1;
  } else {
    inputs[inputIndex][inputCharacterIndex] = c;
    inputCharacterIndex += 1;    
  }
}

void printInput() {
  Serial.print("Received ");
  Serial.print(inputIndex);
  Serial.println(" lines:");
  
  for (int i = 0; i < inputIndex; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(inputs[i]);
  }
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  Serial.println("Waiting for input");
}

void loop() {
  if (loopCount > 1000) {
    // Have looped for approx 10 seconds
    Serial.println("Reached the maximum number of loops");
    Serial.print("Input index ");
    Serial.println(inputIndex);
    printInput();
    delay(1000000);
    return;
  }

  if (inputIndex >= INPUT_COUNT) {
    Serial.println("Finished test");
    printInput();
    delay(1000000);
    return;
  }
  
  // Read bytes until there are no more to read
  for (int byte = Serial.read(); byte != -1; byte = Serial.read()) {
    receiveInput((char) byte);
  }
  
  loopCount += 1;
  delay(20);
}

