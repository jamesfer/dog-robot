import time
import math
from .serial_interface import SerialInterface
from .logger import console


# interface = SerialInterface('/dev/tty.usbmodem1421', baud=9600)
# interface = SerialInterface('/dev/tty.usbmodem1421', baud=38400)
# interface = SerialInterface('/dev/tty.usbmodem1421', baud=57600)
interface = SerialInterface('/dev/tty.usbmodem1421', baud=115200)
interface.listen()
time.sleep(1)

console.log('Starting test')
for i in range(0, 100):
    interface.write('Number %d' % (i,))

interface.flush()

input()
interface.stop()
