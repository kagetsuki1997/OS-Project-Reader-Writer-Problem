import SystemControl

waitingList=[]
starveThreshold=5
priority='Writer'

generator=SystemControl.Generator()
scheduler=SystemControl.Scheduler()
generator.start()
scheduler.start()