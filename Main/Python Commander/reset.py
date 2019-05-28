from SerialInterface import SerialInterface
import time

inter = SerialInterface('/dev/tty.usbmodem1421')
inter.Listen()

joints = [
    'BackRightKnee',
    'BackRightShoulder',
    'BackLeftKnee',
    'BackLeftShoulder',
    'FrontRightKnee',
    'FrontRightShoulder',
    'FrontLeftKnee',
    'FrontLeftShoulder',
]

for j in joints:
    message = 'MoveJoint %s 0' % (j,)
    print(message)
    inter.Write(message)
    time.sleep(1)

inter.Stop()
