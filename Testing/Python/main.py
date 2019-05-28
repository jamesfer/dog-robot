from SerialInterface import SerialInterface
import time
from Logger import console

def increment(message):
    console.log(message)
    if message == "This is message number 0":
        # console.log("Message correct")
        pass
    else:
        console.log("Message incorrect")

interface = SerialInterface('/dev/tty.usbmodem1421', 115200)
interface.Listen()
interface.OnInput(increment)
message_count = 0

last_time = time.time()
while True:
    cur_time = time.time()
    if cur_time - last_time > 1:
        # print('Recieved %s messages' % (message_count,))
        last_time = cur_time
        interface.Write('This is message number %s' % (message_count,))
        console.log('Sending message')
