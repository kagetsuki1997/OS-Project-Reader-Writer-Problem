import threading,globcfg
import time,random


class Reader(threading.Thread):
    def __init__(self, book, lock,number):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Reader'
        self.lock=lock
        self.id = number
        self.on=False

    def run(self):
        self.on=True
        print("[log]thread[{number}] {name} start...".format(number=self.id, name=self.name))
        print("The reader " + str(self.id) + " comes to the reading room")
        self.book.want_to_read()
        print("The reader " + str(self.id) + " begins reading")
        time.sleep(random.expovariate(1/globcfg.lamRW)/10)
        print("The reader " + str(self.id) + " ends reading")
        self.book.end_reading()
        print("The reader " + str(self.id) + " leaves the reading room")
