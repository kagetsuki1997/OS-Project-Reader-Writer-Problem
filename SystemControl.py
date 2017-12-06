import numpy as np
import random,threading,time
import Reader,Writer,globcfg


def getRandomInterval(lam=10):
    #poi=np.random.poisson(lam,1)
    t=random.expovariate(1/lam)/10
    print("[log]randomTime= %.2f"%t)
    return t

def togglePriority():
    if(globcfg.priority=='Writer'):
        return 'Reader'
    else:
        return 'Writer'

def avoidStarvation(currentThreadNumber):
    target=togglePriority()
    print("--Avoid Starvation Progress Start--")
    for thread in globcfg.waitingList:
        if(thread.name==target and thread.number<=currentThreadNumber and not thread.on):
            thread.start()
            #del(thread)
    print("--Avoid Starvation Progress End--")


class Generator(threading.Thread):
    def __init__(self,book):
        super(Generator,self).__init__()
        self.book=book
        self.lock=threading.Lock()
    def run(self):
        print("[log]Generator start...")
        while(True):
            print("[log]currentRunThread: %d"%globcfg.currentRunThreadCount)
            time.sleep(getRandomInterval())
            choice=random.randint(0,1)
            if(choice):
                print("[log]Generate thread {number} : {name}".format(number=globcfg.threadNumber,name="Reader"))
                globcfg.waitingList.append(Reader.Reader(self.book,self.lock,globcfg.threadNumber)) #new Reader
            else:
                print("[log]Generate thread {number} : {name}".format(number=globcfg.threadNumber, name="Writer"))
                globcfg.waitingList.append(Writer.Writer(self.book,self.lock,globcfg.threadNumber)) #new Writer
            globcfg.threadNumber+=1

class Scheduler(threading.Thread):
    def __init__(self):
        super(Scheduler,self).__init__()

    def run(self):
        print("[log]Scheduler start...")
        counter={'Writer':0,'Reader':0}
        currentThreadNumber=0
        while(True):
            for thread in globcfg.waitingList:
                if(thread.name==globcfg.priority and not thread.on):
                    thread.start()
                    counter[globcfg.priority] += 1
                    if (counter[globcfg.priority] >= globcfg.starveThreshold):
                        currentThreadNumber=thread.number
                        avoidStarvation(currentThreadNumber)
                        counter[globcfg.priority]=0
                    #del(thread)
                elif(globcfg.currentRunThreadCount==0 and not thread.on):
                    thread.start()
                    counter[globcfg.priority] = 0
                    #del(thread)
                else:
                    continue



