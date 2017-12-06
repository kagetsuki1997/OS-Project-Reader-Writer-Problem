import SystemControl,Book,globcfg

def main():
    book=Book.Book()
    generator=SystemControl.Generator(book)
    scheduler=SystemControl.Scheduler()

    generator.start()
    scheduler.start()

main()