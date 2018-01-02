import SystemControl,Book,globcfg
import Input_box_lambda
import Button

def main():
    Input_box_lambda
    print ("lamGen= %d" %globcfg.lamGen)
    print ("lamRW= %d" %globcfg.lamRW)
    Button
    print ("Priority: %s" %globcfg.priority)
    book=Book.Book()
    generator=SystemControl.Generator(book)
    scheduler=SystemControl.Scheduler()

    generator.start()
    scheduler.start()



main()
while (True):
    s = input()
    print(s)
    if (s == "w"):
        globcfg.priority = "Writer"
        print("--Set priority: Writer--")
    elif (s == "r"):
        globcfg.priority = "Reader"
        print("--Set priority: Reader--")
