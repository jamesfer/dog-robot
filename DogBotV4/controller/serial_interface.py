import serial
import threading
from .logger import console


# '/dev/tty.usbmodem1421'
class SerialInterface:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.outgoing_buffer = []
        self.incoming_buffer = []
        self.should_flush = False
        self.stopped = False
        self.listen_thread = None
        self.cb = None

    def listen(self):
        self.stopped = False
        self.listen_thread = threading.Thread(target=self._start_listen_loop)
        self.listen_thread.start()

    def write(self, message):
        self.outgoing_buffer.append(str(message))

    def on_input(self, cb):
        self.cb = cb

    def stop(self):
        self.stopped = True
        if self.listen_thread:
            self.listen_thread.join()

    def flush(self):
        self.should_flush = True

    def _start_listen_loop(self):
        with serial.Serial(self.port, self.baud, timeout=0) as ser:
            console.log('Connected to %s (%s)' % (ser.name, ser.baudrate))
            incoming = ''
            while not self.stopped:
                # Send all outgoing messages
                while len(self.outgoing_buffer):
                    message = self.outgoing_buffer.pop(0)
                    # console.log('Sending %s' % (message,))
                    ser.write(bytes(message + '\n', 'ascii'))

                # Read all incoming messages
                incoming += ser.read(ser.in_waiting).decode('ascii')
                incoming = self._process_input(incoming)

                if self.should_flush:
                    ser.flush()

    def _process_input(self, message):
        index = message.find('\r\n')
        while not index == -1:
            line = message[:index]
            console.log(line)
            if self.cb is not None:
                self.cb(line)
            message = message[index + 2:]
            index = message.find('\r\n')
        return message
