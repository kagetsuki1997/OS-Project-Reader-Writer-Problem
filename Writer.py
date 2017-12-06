import threading,globcfg
import time,random


class Writer(threading.Thread):
    def __init__(self, book, lock,number):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Writer'
        self.lock=lock
        self.number = number
        self.on=False

    def run(self):
        self.on=True
        print("[log]thread[{number}] {name} start...".format(number=self.number, name=self.name))
        print ("The writer " + str(self.number) + " comes to the writing room")
        self.book.want_to_write()
        print ("The writer " + str(self.number) + " begins writing")
        time.sleep(random.randint(1,10))
        print ("The writer " + str(self.number) + " ends writing")
        self.book.end_writing()
        print ("The writer " + str(self.number) + " leaves the writing room")

