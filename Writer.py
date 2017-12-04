import threading
import time
import book.py

class Writer(threading.Thread):
    def __init__(self, book, lock):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Writer'
        self.number = set_number(lock)

    def set_number(self, lock):
        lock.acquire()
        global threadNumber
        self.number = threadNumber
        threadNumber+=1
        lock.release()

    def run(self):
        print ("The writer " + str(self.number) + "comes to the writing room")
        self.book.want_to_write()
        print ("The writer " + str(self.number) + "begins writing")
        self.sleep(6)
        print ("The writer " + str(self.number) + "ends writing")
        self.book.end_writing()
        print ("The writer " + str(self.number) + "leaves the writing room")
