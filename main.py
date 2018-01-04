import SystemControl,Book,globcfg
import Input_box_lambda
import Button
from Gui import Gui

def main():
    Input_box_lambda
    print ("lamGen= %d" %globcfg.lamGen)
    print ("lamRW= %d" %globcfg.lamRW)
    Button
    print ("Priority: %s" %globcfg.priority)
    book=Book.Book()
    g = Gui()
    generator=SystemControl.Generator(book, g)
    scheduler=SystemControl.Scheduler()


    generator.start()
    scheduler.start()

    # start Gui
    g.animation(50, 50, 5)

main()

