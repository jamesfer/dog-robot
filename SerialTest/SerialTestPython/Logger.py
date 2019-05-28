import threading


class Logger:
    def __init__(self):
        self.lock = threading.Lock()

    def log(self, message):
        self.lock.acquire()
        print(message)
        self.lock.release()


console = Logger()
