import threading
import time
from GG import Gui

class Reader(threading.Thread):
    def __init__(self, book, tid, g):
        threading.Thread.__init__(self)
        self.book = book
        self.tid = tid
        self.gui = g

    def run(self):
        print("The reader " + str(self.tid) + " comes to the reading room")
        self.gui.change_state("R", self.tid, self.gui.scheduling, self.gui.r_waiting)
        self.book.want_to_read()
        print("The reader " + str(self.tid) + " begins reading")
        self.gui.change_state("R", self.tid, self.gui.r_waiting, self.gui.filing)
        time.sleep(3)
        print("The reader " + str(self.tid) + " ends reading")
        self.gui.change_state("R", self.tid, self.gui.filing, self.gui.scheduling)
        self.book.end_reading()
        print("The reader " + str(self.tid) + " leaves the reading room")
