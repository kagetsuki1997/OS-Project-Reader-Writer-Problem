import numpy as np
import random,threading,time
import Reader,Writer,globcfg


def getRandomInterval(lam=10):
    #poi=np.random.poisson(lam,1)
    t=random.expovariate(1/lam)/10
    #print("[log]randomTime= %.2f"%t)
    return t

def togglePriority():
    if(globcfg.priority=='Writer'):
        return 'Reader'
    else:
        return 'Writer'

def avoidStarvation(currentThreadId):
    target=togglePriority()
    print("**Starvation Detected**\n {priority}s, you are too greedy!\nLet's give {target} a chance~".format(priority=globcfg.priority,target=target))

    while(globcfg.currentRunThreadCount['Writer']!=0 or globcfg.currentRunThreadCount['Reader']!=0):
        print("[avoidStarvation]Wait for current running threads done...")
        time.sleep(1)

    print("--Avoid Starvation Progress Start--")

    for thread in globcfg.waitingList:
        if(thread.name==target and thread.id <= currentThreadId and not thread.on):
            globcfg.currentRunThreadCount[target] += 1
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
            print("[log]currentRunThread: Reader= {readCount}, Writer= {writeCount}".format(readCount=globcfg.currentRunThreadCount['Reader'],writeCount=globcfg.currentRunThreadCount['Writer']))
            time.sleep(getRandomInterval(globcfg.lamGen))
            choice=random.randint(0,1)
            #noWhere→scheduling(產生thread到scheduler但還沒run)
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

        while(True):
            for thread in globcfg.waitingList:
                #Scheduling→wait
                if(thread.name==globcfg.priority and not thread.on):
                    globcfg.currentRunThreadCount[globcfg.priority]+=1
                    thread.start()
                    counter[globcfg.priority] += 1
                    if (counter[globcfg.priority] >= globcfg.starveThreshold):
                        currentThreadId=thread.id
                        avoidStarvation(currentThreadId)
                        counter[globcfg.priority]=0
                    #del(thread)
                elif(globcfg.currentRunThreadCount['Writer']==0 and globcfg.currentRunThreadCount['Reader']==0 and not thread.on):
                    globcfg.currentRunThreadCount[togglePriority()]+=1
                    print("[log]No thread running!~")
                    thread.start()
                    counter[globcfg.priority] = 0
                    #del(thread)
                else:
                    continue



