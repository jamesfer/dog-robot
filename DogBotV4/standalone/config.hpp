struct GaitStep {
  GaitStep(float shoulderAngle, float kneeAngle): shoulderAngle(shoulderAngle), kneeAngle(kneeAngle) {}
  float shoulderAngle;
  float kneeAngle;
};

struct Joint {
  Joint(int pin, int offset): pin(pin), offset(offset) {}
  int pin;
  int offset;
};

struct Leg {
  Leg(Joint knee, Joint shoulder, int timeOffset, bool invert): knee(knee), shoulder(shoulder), timeOffset(timeOffset), invert(invert) {}
  Joint knee;
  Joint shoulder;
  int timeOffset;
  bool invert;
};

const int loopDelay = 10;
const int gaitPeriod = 1000;
const int gaitStepCount = 27;
const int gaitStepInterval = gaitPeriod / (gaitStepCount + 1);
const int legCount = 4;
const int gaitLegPeriod = gaitPeriod / legCount;

const Leg legs[legCount] = {
  // Front left
  Leg{Joint{4, 10}, Joint{5, 135}, gaitLegPeriod * 0, true},
  // Front right
  Leg{Joint{7, 0}, Joint{6, 140}, gaitLegPeriod * 2, false},
  // Back left
  Leg{Joint{11, -20}, Joint{10, 130}, gaitLegPeriod * 3, true},
  // Back right
  Leg{Joint{8, 10}, Joint{9, 140}, gaitLegPeriod * 1, false}
};

const GaitStep gait[gaitStepCount] = {
    GaitStep{-0.4931828728, 1.3589035},
    GaitStep{-0.5505394628, 1.378092398},
    GaitStep{-0.6056474798, 1.391495988},
    GaitStep{-0.6583129916, 1.399161001},
    GaitStep{-0.7083188835, 1.401111636},
    GaitStep{-0.7554332537, 1.397353763},
    GaitStep{-0.7994166264, 1.38787597},
    GaitStep{-0.8400275485, 1.372647537},
    GaitStep{-0.8770260425, 1.351613181},
    GaitStep{-0.9101743281, 1.324684204},
    GaitStep{-0.9392341448, 1.291725244},
    GaitStep{-0.9699039563, 1.240756382},
    GaitStep{-0.9943380042, 1.174225065},
    GaitStep{-1.021943166, 1.080418181},
    GaitStep{-1.078271702, 1.192418054},
    GaitStep{-1.140570746, 1.398768458},
    GaitStep{-1.144951919, 1.586701077},
    GaitStep{-1.136534104, 1.796906384},
    GaitStep{-1.084210771, 1.849677719},
    GaitStep{-0.9441769963, 1.897398987},
    GaitStep{-0.8129540492, 1.847133145},
    GaitStep{-0.6433923303, 1.72473099},
    GaitStep{-0.468505477, 1.575017355},
    GaitStep{-0.3683909042, 1.419568283},
    GaitStep{-0.3673002921, 1.306524801},
    GaitStep{-0.427525354, 1.33072954},
    GaitStep{-0.4931828728, 1.3589035}
};
