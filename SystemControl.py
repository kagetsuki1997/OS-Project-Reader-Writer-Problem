import numpy as np

def getRandomInterval(lam=10):
    poi=np.random.poisson(lam,1)
    return poi[0]
