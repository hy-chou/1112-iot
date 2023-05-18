from sys import argv
from json import loads
from math import sqrt

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


def getTops(targetSL, k=9):
    data = getData()
    for i in range(len(data)):
        data[i].append(euDist(targetSL, data[i][1]))
    dataSorted = sorted(data, key=lambda x: x[2])

    tops = []
    weights = []
    for i in range(k):
        weights.append(1 / ((dataSorted[i][2] + 1e-2) ** 2))
        tops.append(dataSorted[i][0])

    return np.average(tops, weights=weights, axis=0)


if __name__ == '__main__':
    target = [argv[i] for i in range(2, 6)]
    res = getTops(target)
    print(res)
