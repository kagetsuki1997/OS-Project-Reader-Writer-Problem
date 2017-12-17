from Writer import Writer
from Reader import Reader
from Book import Book
from GG import Gui
from GG import GuiRunner

def main():
    b = Book()
    g = Gui()
    GuiRunner(g, "animation").start()

    g.change_state("W", 7, g.nowhere, g.scheduling)
    Writer(b, 7, g).start()
    for i in range(0, 3):
        g.change_state("R", i, g.nowhere, g.scheduling)
        Reader(b, i, g).start()

    for i in range(0, 2):
        g.change_state("W", i, g.nowhere, g.scheduling)
        Writer(b, i, g).start()

main()
