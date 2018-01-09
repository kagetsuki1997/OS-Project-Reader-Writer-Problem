import threading
waitingList=[]
starveThreshold=5
priority='Writer'
threadNumber=0
currentRunThreadCount={'Writer':0,'Reader':0} #the thread which is "start"
global lamGen
lamGen = 10 #average time is lamGen/10
global lamRW
lamRW = 20 #average time is lamRW/10
event=threading.Event()

# To print extra info
global inAvoidStarvation
inAvoidStarvation = False
global inAvoidStarvation_lock
inAvoidStarvation_lock = threading.Lock()
global generate_time_globalCopy
generate_time_globalCopy = 0
global generateTime_lock
generateTime_lock = threading.Lock()
global executionTime_globalcopy
executionTime_globalcopy = 0
global executionTime_globalcopy_lock
executionTime_globalcopy_lock = threading.Lock()
