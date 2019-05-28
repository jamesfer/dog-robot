#include <Servo.h>
#include "config.hpp"

unsigned long startTime;
Servo servos[legCount * 2];

enum JointType : int {
  Knee = 0,
  Shoulder = 1
};

Servo& servoFor(int legIndex, JointType joint) {
  return servos[legIndex * 2 + joint];
}

const GaitStep& stepAtTime(unsigned long time, int legIndex) {
  unsigned long gaitTime = (time + legs[legIndex].timeOffset) % gaitPeriod;
  int stepIndex = gaitTime / gaitStepInterval;

//  Serial.println(stepIndex);

  return gait[stepIndex];
}

int toDegrees(float radians) {
  return int (radians * 180.f / 3.14159265359);
}

void writePosition(int legIndex, const GaitStep& gaitStep) {
  Leg leg = legs[legIndex];
  int kneeAngle = toDegrees(gaitStep.kneeAngle) + leg.knee.offset;
  servoFor(legIndex, Knee).write(leg.invert ? 180 - kneeAngle : kneeAngle);
  int shoulderAngle = toDegrees(gaitStep.shoulderAngle) + leg.shoulder.offset;
  servoFor(legIndex, Shoulder).write(leg.invert ? 180 - shoulderAngle : shoulderAngle);
}

void setup() {
  Serial.begin(115200);
  startTime = millis();

  // Attach each leg's servos
  for (int l = 0; l < legCount; l++) {
    servoFor(l, Knee).attach(legs[l].knee.pin);
    servoFor(l, Shoulder).attach(legs[l].shoulder.pin);
  }
}

void loop() {
  unsigned long currentTime = millis();

  // Write a position to each of the legs
  for (int l = 0; l < legCount; l++) {
    GaitStep step = stepAtTime(currentTime, l);
    writePosition(l, step);
  }

  delay(loopDelay);
}
