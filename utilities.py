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
    elif loadType == 'representative':
        x = np.asarray([
            276.838051451739,
            236.45419896787254,
            204.39592817699,
            209.7792272946393,
            226.29793364246785,
            322.4237952788615,
            456.53907434123124,
            631.1062745205518,
            685.7427864634963,
            749.8898722566746,
            748.9092102267244,
            753.3564449967976,
            704.3347956265558,
            685.7533273837373,
            921.9092505062281,
            1084.2080292838439,
            1329.4459849798664,
            1464.5549435073706,
            1380.6552972939141,
            1235.305140696039,
            899.3667895183373,
            698.7389208351024,
            449.2279441610577,
            349.60868234099854
        ])
        return x/np.sum(x)
    else:
        raise ArgumentError('Unrecognized load profile type')
