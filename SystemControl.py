import random,threading,time
import Reader,Writer,globcfg


def getRandomInterval(lam=10):
    t=random.expovariate(10/lam)
    return t

def togglePriority():
    if(globcfg.priority=='Writer'):
        return 'Reader'
    else:
        return 'Writer'

def avoidStarvation(currentThreadId):
    target=togglePriority()

    globcfg.inAvoidStarvation_lock.acquire()
    globcfg.inAvoidStarvation = True
    globcfg.inAvoidStarvation_lock.release()

    print("**Starvation Detected**\n {priority}s, you are too greedy!\nLet's give {target} a chance~".format(priority=globcfg.priority,target=target))

    while(globcfg.currentRunThreadCount['Writer']!=0 or globcfg.currentRunThreadCount['Reader']!=0):
        print("[avoidStarvation]Wait for current running threads done...")
        time.sleep(1)

    print("--Avoid Starvation Progress Start--")

    
    for thread in globcfg.waitingList:
        if(thread.name==target and thread.id <= currentThreadId and not thread.on):
            globcfg.currentRunThreadCount[target] += 1
            thread.start()        
            
    print("--Avoid Starvation Progress End--")
    globcfg.inAvoidStarvation_lock.acquire()
    globcfg.inAvoidStarvation = False
    globcfg.inAvoidStarvation_lock.release()


class Generator(threading.Thread):
    def __init__(self,book, g):
        super(Generator,self).__init__()
        self.book=book
        self.gui = g
        self.lock=threading.Lock()
    def run(self):
        print("[log]Generator start...")
        while(not globcfg.event.is_set()):
            print("[log]currentRunThread: Reader= {readCount}, Writer= {writeCount}".format(readCount=globcfg.currentRunThreadCount['Reader'],writeCount=globcfg.currentRunThreadCount['Writer']))
            genterate_time=getRandomInterval(globcfg.lamGen)
            globcfg.generateTime_lock.acquire()
            globcfg.generate_time_globalCopy = genterate_time
            globcfg.generateTime_lock.release()
            globcfg.event.wait(genterate_time)
            choice=random.randint(0,1)
            # generate a new thread

            if(choice):
                print("[log]Generate thread {number} : {name}".format(number=globcfg.threadNumber,name="Reader"))
                self.gui.change_state("R", globcfg.threadNumber, self.gui.nowhere, self.gui.scheduling)
                globcfg.waitingList.append(Reader.Reader(self.book,self.lock,globcfg.threadNumber, self.gui)) #new Reader
            else:
                print("[log]Generate thread {number} : {name}".format(number=globcfg.threadNumber, name="Writer"))
                self.gui.change_state("W", globcfg.threadNumber, self.gui.nowhere, self.gui.scheduling)
                globcfg.waitingList.append(Writer.Writer(self.book,self.lock,globcfg.threadNumber, self.gui)) #new Writer
            globcfg.threadNumber+=1

class Scheduler(threading.Thread):
    def __init__(self):
        super(Scheduler,self).__init__()

    def run(self):
        print("[log]Scheduler start...")
        counter={'Writer':0,'Reader':0}

        while(not globcfg.event.is_set()):
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
                elif(globcfg.currentRunThreadCount[globcfg.priority]==0  and not thread.on):
                    globcfg.currentRunThreadCount[togglePriority()]+=1
                    print("[log]No thread running!~")
                    thread.start()
                    counter[globcfg.priority] = 0
                    #del(thread)
                else:
                    continue



