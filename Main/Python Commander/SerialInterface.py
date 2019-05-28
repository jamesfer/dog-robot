import serial
import threading
import time
from Logger import console

# '/dev/tty.usbmodem1421'
class SerialInterface:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.outgoing_buffer = []
        self.incoming_buffer = []
        self.stopped = False
        self.listen_thread = None
        self.cb = None

    def Listen(self):
        self.stopped = False
        self.listen_thread = threading.Thread(target=self._startListenLoop)
        self.listen_thread.start()

    def Write(self, message):
        self.outgoing_buffer.append(message)

    def OnInput(self, cb):
        self.cb = cb

    def Stop(self):
        self.stopped = True
        if self.listen_thread:
            self.listen_thread.join()

    def _startListenLoop(self):
        with serial.Serial(self.port, self.baud, timeout=0) as ser:
            console.log('Connected to %s (%s)' % (ser.name, ser.baudrate))
            incoming = ''
            while not self.stopped:
                # Send all outgoing messages
                while len(self.outgoing_buffer):
                    message = self.outgoing_buffer.pop(0) + '\n'
                    # console.log('Sending %s' % (message,))
                    ser.write(bytes(message, 'ascii'))

                # Read all incoming messages
                incoming += ser.read(ser.in_waiting).decode('ascii')
                incoming = self._processInput(incoming)

    def _processInput(self, message):
        index = message.find('\r\n')
        while not index == -1:
            line = message[:index]
            console.log(line)
            if not self.cb == None:
                self.cb(line)
            message = message[index + 2:]
            index = message.find('\r\n')
        return message
