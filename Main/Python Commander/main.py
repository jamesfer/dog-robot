from SerialInterface import SerialInterface
import time
import math
from Logger import console

coords = [
    (0.00, -0.4931828728, 1.3589035),
    (33.37, -0.5505394628, 1.378092398),
    (66.73, -0.6056474798, 1.391495988),
    (100.10, -0.6583129916, 1.399161001),
    (133.47, -0.7083188835, 1.401111636),
    (166.83, -0.7554332537, 1.397353763),
    (200.20, -0.7994166264, 1.38787597),
    (233.57, -0.8400275485, 1.372647537),
    (266.93, -0.8770260425, 1.351613181),
    (300.30, -0.9101743281, 1.324684204),
    (333.67, -0.9392341448, 1.291725244),
    (367.03, -0.9699039563, 1.240756382),
    (400.40, -0.9943380042, 1.174225065),
    (433.77, -1.021943166, 1.080418181),
    (467.13, -1.078271702, 1.192418054),
    (500.50, -1.140570746, 1.398768458),
    (533.87, -1.144951919, 1.586701077),
    (567.23, -1.136534104, 1.796906384),
    (600.60, -1.084210771, 1.849677719),
    (633.97, -0.9441769963, 1.897398987),
    (667.33, -0.8129540492, 1.847133145),
    (700.70, -0.6433923303, 1.72473099),
    (734.07, -0.468505477, 1.575017355),
    (767.43, -0.3683909042, 1.419568283),
    (800.80, -0.3673002921, 1.306524801),
    (834.17, -0.427525354, 1.33072954),
    (867.53, -0.4931828728, 1.3589035)
]

total_time = 10
interval = 1
time_factor = 0.5
stride_duration = coords[-1][0]
time_offset = stride_duration / 4
legs = [
    ('FrontLeft', time_offset * 1),
    ('BackRight', time_offset * 2),
    ('FrontRight', time_offset * 3),
    # ('BackLeft', time_offset * 4),
]

def toDegreeInt(num):
    return int(num * 180 / math.pi)

def getStep(time):
    for s in coords[::-1]:
        if s[0] < time:
            return s
    return coords[-1]



inter = SerialInterface('/dev/tty.usbmodem1421', baud=115200)
inter.Listen()
time.sleep(1)

initial_time = time.time()
last_time = initial_time

while time.time() - initial_time < total_time:
    cur_time = time.time()
    if cur_time - last_time > interval:
        last_time = cur_time
        diff_ms = (cur_time - initial_time) * 1000

        for leg in legs:
            leg_time = (diff_ms * time_factor + leg[1]) % stride_duration
            step = getStep(leg_time)
            kneeAngle = toDegreeInt(step[2])
            shoulderAngle = toDegreeInt(step[1])
            inter.Write('MoveJoint %s%s %s' % (leg[0], 'Knee', kneeAngle))
            # inter.Write('MoveJoint %s%s %s' % (leg[0], 'Shoulder', shoulderAngle))

inter.Stop()
