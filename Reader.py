import threading,globcfg
import time,random


class Reader(threading.Thread):
    def __init__(self, book, lock,number):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Reader'
        self.lock=lock
        self.number = number
        self.on=False

    def run(self):
        self.on=True
        print("[log]thread[{number}] {name} start...".format(number=self.number, name=self.name))
        print("The reader " + str(self.number) + " comes to the reading room")
        self.book.want_to_read()
        print("The reader " + str(self.number) + " begins reading")
        time.sleep(random.randint(1,10))
        print("The reader " + str(self.number) + " ends reading")
        self.book.end_reading()
        print("The reader " + str(self.number) + " leaves the reading room")
