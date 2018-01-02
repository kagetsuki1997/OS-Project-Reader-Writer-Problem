waitingList=[]
starveThreshold=5
priority='Writer_priority'
threadNumber=0
currentRunThreadCount={'Writer':0,'Reader':0} #the thread which is "start"
global lamGen
lamGen = 10 #average time is lamGen/10
global lamRW
lamRW = 50 #average time is lamRW/10
