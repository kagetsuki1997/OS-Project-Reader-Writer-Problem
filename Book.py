import threading


class Book:
    def __init__(self):
        self.writers = 0
        self.readers = 0
        self.lock = threading.Lock()
        self.condR = threading.Condition(self.lock)
        self.condW = threading.Condition(self.lock)

    def want_to_read(self):
        self.condR.acquire()
        try:
            while self.writers > 0:
                self.condR.wait()
            self.readers += 1
            self.condR.notify()
        finally:
            global currentRunThreadCount
            currentRunThreadCount = currentRunThreadCount + 1
            self.condR.release()

    def end_reading(self):
        self.condR.acquire()
        try:
            self.readers -= 1
            if self.readers == 0:
                self.condW.notify()
        finally:
            global currentRunThreadCount
            currentRunThreadCount = currentRunThreadCount - 1
            self.condR.release()

    def want_to_write(self):
        self.condR.acquire()
        try:
            while self.writers > 0 or self.readers > 0:
                self.condW.wait()
            self.writers += 1
        finally:
            global currentRunThreadCount
            currentRunThreadCount = currentRunThreadCount + 1
            self.condR.release()

    def end_writing(self):
        self.condR.acquire()
        try:
            self.writers -= 1
            if self.writers == 0:
                self.condR.notify()
            self.condW.notify()
        finally:
            global currentRunThreadCount
            currentRunThreadCount = currentRunThreadCount - 1
            self.condR.release()
