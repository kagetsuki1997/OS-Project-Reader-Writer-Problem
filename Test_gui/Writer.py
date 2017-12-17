# -*- coding: utf-8 -*-
__author__ = 'Konrad'

import threading
import time
from GG import Gui

class Writer(threading.Thread):
    def __init__(self, book, tid, g):
        threading.Thread.__init__(self)
        self.book = book
        self.tid = tid
        self.gui = g

    def run(self):
        print("The writer " + str(self.tid) + " comes to the reading room")
        self.gui.change_state("W", self.tid, self.gui.scheduling, self.gui.w_waiting)
        self.book.want_to_write()
        print("The writer " + str(self.tid) + " begins writing")
        self.gui.change_state("W", self.tid, self.gui.w_waiting, self.gui.filing)
        time.sleep(6)
        print("The writer " + str(self.tid) + " ends writing")
        self.gui.change_state("W", self.tid, self.gui.filing, self.gui.scheduling)
        self.book.end_writing()
        print("The writer " + str(self.tid) + " leaves the reading room")
