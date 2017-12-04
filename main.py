import SystemControl

def main():
    waitingList=[]
    starveThreshold=5
    priority='Writer'
    threadNumber=0
    currentRunThreadCount=0

    generator=SystemControl.Generator()
    scheduler=SystemControl.Scheduler()
    generator.start()
    scheduler.start()

main()