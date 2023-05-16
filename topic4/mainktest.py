from json import loads
from math import sqrt, ceil

import numpy as np


def getData(filepath='./data.json'):
    with open(filepath) as f:
        lines = f.readline()
    return loads(lines)

def euDist(SL1, SL2):
    validDim = 0
    d2 = 0

    for i in range(len(SL1)):
        if (SL1[i] == -99 or SL2[i] == -99):
            continue
        d2 += (SL1[i] - SL2[i]) ** 2
        validDim += 1

    return sqrt(d2) / validDim


def getTops(targetSL, k=10):
    data = getData()
    for i in range(len(data)):
        data[i].append(euDist(targetSL, data[i][1]))
    dataSorted = sorted(data, key=lambda x: x[2])

    tops = []
    for i in range(k):
        rangelimit = 1.7
        if (i > 0) and (dataSorted[i][2] > rangelimit):
            break
        for _ in range(ceil((k - i)**2)):
            tops.append(dataSorted[i][0])

    return np.mean(tops, axis=0)


if __name__ == '__main__':
    for kvalue in range(9, 11):
        print(kvalue, end='\t')

        for testing in ['./data.json', './testing.json']:
            err = 0
            testing = getData(testing)
            for testee in testing:
                res = getTops(testee[1], kvalue)
                err += euDist(res, testee[0])
            print(err, end='\t')
        print()
