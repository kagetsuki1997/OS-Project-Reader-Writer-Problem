import threading,globcfg
import random
from Gui import Gui

class Writer(threading.Thread):
    def __init__(self, book, lock, number, g):
        threading.Thread.__init__(self)
        self.book = book
        self.name = 'Writer'
        self.lock=lock
        self.id = number
        self.on=False
        self.gui = g

    def run(self):
        self.on=True
        print("[log]thread[{number}] {name} start...".format(number=self.id, name=self.name))
        print ("The writer " + str(self.id) + " comes to the writing room")
        self.gui.change_state("W", self.id, self.gui.scheduling, self.gui.w_waiting)
        self.book.want_to_write()
        print ("The writer " + str(self.id) + " begins writing")
        self.gui.change_state("W", self.id, self.gui.w_waiting, self.gui.filing)
        execute_time=random.expovariate(10 / globcfg.lamRW)
        globcfg.executionTime_globalcopy_lock.acquire()
        globcfg.executionTime_globalcopy = execute_time
        globcfg.executionTime_globalcopy_lock.release()
        globcfg.event.wait(execute_time)
        print ("The writer " + str(self.id) + " ends writing")
        self.gui.change_state("W", self.id, self.gui.filing, self.gui.nowhere)
        self.book.end_writing()
        print ("The writer " + str(self.id) + " leaves the writing room")


