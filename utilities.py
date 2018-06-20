import numpy as np

def getReliabilityValue(r):
    return 1-0.1/(2.**r)

def getLoadProfile(loadType):
    if loadType == 'constant':
        return np.ones(24)/24
    elif loadType == 'dayHeavy':
        x = np.zeros(24)
        x[6:17] = 1
        return x/np.sum(x)
    elif loadType == 'nightHeavy':
        x = np.ones(24)
        x[6:17] = 0
        return x/np.sum(x)
