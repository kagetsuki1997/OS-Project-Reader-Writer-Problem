import numpy as np
import random,threading,time

def getRandomInterval(lam=10):
    poi=np.random.poisson(lam,1)
    return poi[0]

def togglePriority():
    global priority
    if(priority=='Writer'):
        return 'Reader'
    else:
        return 'Writer'

def avoidStarvation(currentThreadNumber):
    global priority,waitingList
    for thread in waitingList:
        #TODO


class Generator(threading.Thread):
    def __init__(self):
        super(Generator,self).__init__()
    def run(self):
        global waitingList,starveThreshold
        while(True):
            time.sleep(getRandomInterval())
            choice=random.randint(0,1)
            if(choice):
                waitingList.append(#reader TODO)
            else:
                waitingList.append(#writer TODO)

class Scheduler(threading.Thread):
    def __init__(self):
        super(Scheduler,self).__init__()

    def run(self):
        global waitingList
        global starveThreshold
        global priority
        counter={'Writer':0,'Reader':0}
        currentThreadNumber=0
        while(True):
            for thread in waitingList:
                if(thread.name==priority):
                    thread.start()
                    counter[priority] += 1
                    if (counter[priority] >= starveThreshold):
                        currentThreadNumber=thread.number
                        avoidStarvation(currentThreadNumber)
                        counter[priority]=0
                    del(thread)
                else:
                    continue



