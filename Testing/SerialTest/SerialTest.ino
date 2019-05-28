void setup() {
  Serial.begin(115200);
}

int number = 1;
char buffer[256];
int bufferIndex = 0;
char c;

void loop() {
  for (int byte = Serial.read(); byte != -1; byte = Serial.read())
  {
    c = (char) byte;
    if (c == '\n')
    {
//      Serial.println("Received message");
//      Serial.println(bufferIndex);
      buffer[bufferIndex] = '\0';
      Serial.println(buffer);
      for (int i = 0; i < bufferIndex; i++)
      {
        buffer[bufferIndex] = '\0';
      }
      bufferIndex = 0;
      break;
    }
    buffer[bufferIndex] = c;
    bufferIndex++;
  }
  delay(10);
}
