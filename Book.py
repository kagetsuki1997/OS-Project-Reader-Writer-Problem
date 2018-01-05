import threading,globcfg

class Book:
    def __init__(self):
        self.writers = 0 #current writing 0~1
        self.readers = 0 #current reading 0~
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
            self.condR.release()

    def end_reading(self):
        self.condR.acquire()
        try:
            self.readers -= 1
            globcfg.currentRunThreadCount['Reader'] -= 1
            if(self.readers == 0):
                print("No reader, so it's a chance for writer!")
                self.condW.notify()
        finally:
            self.condR.release()

    def want_to_write(self):
        self.condR.acquire()
        try:
            while self.writers > 0 or self.readers > 0:
                self.condW.wait()
            self.writers += 1
        finally:
            self.condR.release()

    def end_writing(self):
        self.condR.acquire()
        try:
            self.writers -= 1
            globcfg.currentRunThreadCount['Writer'] -= 1
            if( (globcfg.priority=='Reader' or globcfg.currentRunThreadCount['Writer']==0) and self.writers == 0 ):
                if(globcfg.priority=='Writer'):
                    print("The priority is Writer, but there is no writer waiting, so it's a chance for reader!")
                self.condR.notify()
            self.condW.notify()
        finally:
            self.condR.release()
