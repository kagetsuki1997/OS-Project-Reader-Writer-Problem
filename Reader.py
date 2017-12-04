import threading
import time


class Reader(threading.Thread):
    def __init__(self, book, lock):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Reader'
        self.number = 0
        set_number(lock)
        
    def set_number(self, lock):
        lock.acquire()
        global threadNumber
        self.number = threadNumber
        threadNumber = threadNumber + 1
        lock.release()

    def run(self):
        print("The reader " + str(self.number) + " comes to the reading room")
        self.book.want_to_read()
        print("The reader " + str(self.number) + " begins reading")
        time.sleep(3)
        print("The reader " + str(self.number) + " ends reading")
        self.book.end_reading()
        print("The reader " + str(self.number) + " leaves the reading room")
