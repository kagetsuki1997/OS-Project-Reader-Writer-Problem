import SystemControl,Book,globcfg

def main():
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