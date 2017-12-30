from Writer import Writer
from Reader import Reader
from Book import Book
from GG import Gui
from GG import GuiRunner

def main():
    b = Book()
    g = Gui()
    # GuiRunner(g, "animation").start()
    # Don't know why I(linux mint) can but other member(windows) will get error with this.
    # alternatively we don't assingn a thread to  gui but make it operate in main
    
    g.change_state("W", 7, g.nowhere, g.scheduling)
    Writer(b, 7, g).start()
    for i in range(0, 3):
        g.change_state("R", i, g.nowhere, g.scheduling)
        Reader(b, i, g).start()

    for i in range(0, 2):
        g.change_state("W", i, g.nowhere, g.scheduling)
        Writer(b, i, g).start()
        
    g.animation(50, 50, 5)
    # alternative method for problems described above 
        
main()
