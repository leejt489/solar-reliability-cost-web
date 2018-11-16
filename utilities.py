import numpy as np


def getReliabilityValue(r):
    return 1-0.1/(2.**r)


def getLoadProfile(loadType):
    if loadType == 'constant':
        x = np.ones(24)/24
    elif loadType == 'dayHeavy':
        x = np.zeros(24)
        x[6:18] = 1
    elif loadType == 'nightHeavy':
        x = np.ones(24)
        x[6:18] = 0
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
    elif loadType == 'smallIndia':
        # Contact Maria Otero for references mariao14@berkeley.edu
        x = np.asarray([
            0.101260445,
            0.11667435,
            0.12,
            0.13579144,
            0.26028094,
            0.2484019,
            0.1430415,
            0.09611446,
            0.06481775,
            0.06849689,
            0.068364624,
            0.18116747,
            0.1653568,
            0.10288359,
            0.11049436,
            0.155,
            0.367,
            0.486,
            0.50713184,
            0.549,
            0.39770755,
            0.28,
            0.26120673,
            0.112983185,
        ])
    elif loadType == 'mediumHouseholds':
        x = np.asarray([
            0.09324568,
            0.09441229,
            0.10896718,
            0.11666126,
            0.2298227,
            0.23148929,
            0.22696172,
            0.14777094,
            0.13688255,
            0.13235498,
            0.14004907,
            0.1664923,
            0.18674135,
            0.2,
            0.2026295,
            0.193,
            0.19324106,
            0.3432341,
            0.43781305,
            0.49572705,
            0.5096153,
            0.43075784,
            0.2586547,
            0.16740892,
        ])
    elif loadType == 'saGrid':
        x = np.asarray([
            0.5786802,
            0.5329949,
            0.5025381,
            0.4568528,
            0.5939086,
            0.9441624,
            1.5685279,
            1.5989847,
            1.3248731,
            1.2791878,
            1.1269035,
            1.0659899,
            0.9898477,
            1.0203046,
            1.035533,
            1.1116751,
            1.35533,
            1.6903553,
            2.0253806,
            2.071066,
            1.9340101,
            1.6751269,
            1.1573604,
            0.79187816
        ])
    elif loadType == 'loadZim':
        x = np.asarray([
            0.07946235,
            0.083475605,
            0.09584979,
            0.18378456,
            0.37220666,
            0.23370492,
            0.27548733,
            0.185,
            0.13266021,
            0.082182445,
            0.08202637,
            0.12369729,
            0.21582367,
            0.09406612,
            0.077098995,
            0.081156835,
            0.20668238,
            0.42032105,
            0.68006754,
            0.55835456,
            0.5036852,
            0.38194993,
            0.1386578,
            0.071435854
        ])
    elif loadType == 'homeBusiness':
        x = np.asarray([
            0.0587,
            0.0538,
            0.0508,
            0.0505,
            0.0575,
            0.0681,
            0.0838,
            0.102,
            0.119,
            0.185,
            0.287,
            0.31,
            0.298,
            0.235,
            0.189,
            0.171,
            0.168,
            0.154,
            0.288,
            0.372,
            0.352,
            0.231,
            0.135,
            0.0774,
        ])
    elif loadType == 'onlyBusinesses':
        x = np.asarray([
            0.0042,
            0.0032,
            0.0031,
            0.0037,
            0.0078,
            0.0257,
            0.0452,
            0.0808,
            0.128,
            0.169,
            0.194,
            0.198,
            0.196,
            0.19,
            0.184,
            0.171,
            0.153,
            0.165,
            0.235,
            0.235,
            0.167,
            0.0751,
            0.0233,
            0.009
        ])
    else:
        raise ValueError('Unrecognized load profile type')

    return x/np.sum(x)

def calculateMinimumCost(reliabilityFrontier,reliability,dailyLoad,peakCapacity,solarDerate,storageCost,solarCost,chargeControllerCost,capacityCost,fixedCost,oAndMFactor,discountRate,term,batteryLifetime):

    rKey = '{:f}'.format(reliability)

    solarTotalCost = solarCost/solarDerate+chargeControllerCost #Solar lifetime assumed to be term
    storageTotalCost = storageCost*(1-(1-discountRate)**term)/(1-(1-discountRate)**batteryLifetime) #Includes replacement cost of storage
    crf = (discountRate*(1+discountRate)**term)/(((1+discountRate)**term)-1)

    storVals = np.array(reliabilityFrontier['rf'][rKey]['stor'])*dailyLoad
    storCost = storVals*storageTotalCost
    solVals = np.array(reliabilityFrontier['rf'][rKey]['sol'])*dailyLoad
    solCost = solVals*solarTotalCost
    minInd = np.argmin(storCost+solCost)
    capitalCost = storCost[minInd]+solCost[minInd]+peakCapacity*capacityCost+fixedCost
    initialCost = storVals[minInd]*storageCost+solCost[minInd]+peakCapacity*capacityCost+fixedCost #Storage initial cost excludes replacement
    return dict(
        LCOE = (crf+oAndMFactor)*capitalCost/365/dailyLoad/reliability,
        capitalCost = capitalCost,
        initialCost = initialCost,
        replacementCost = capitalCost-initialCost,
        oAndMCost = capitalCost*oAndMFactor,
        solarCapacity = solVals[minInd],
        storageCapacity = storVals[minInd]
    )
