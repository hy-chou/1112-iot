from sys import argv

from os import listdir


macs = [
    '00:11:32:9D:2B:30',
    '00:11:32:9D:30:3A',
    '00:11:32:AD:8C:82',
    '00:11:32:AD:8E:B7',
]

sampleSet = []

files = sorted(listdir('./data-raw'))
for file in files:
    coords = [int(r) for r in file[:-4].split('-')]

    signalLevels = [-999, -999, -999, -999]

    with open(f'./data-raw/{file}') as f:
        lines = f.readlines()
    for line in lines:
        if not line.startswith('00:11:32'):
            continue

        mac = line[:17]
        macID = macs.index(mac)

        p = line.find('Signallevel=') + 12
        signalLevel = int(line[p:-1])

        # select the strongest signal level for each AP
        if signalLevel > signalLevels[macID]:
            signalLevels[macID] = signalLevel

    sampleSet.append([coords, signalLevels])


def coordinate(targetSignalLevels):
    returnValue = []
    for sample in sampleSet:
        coords, signalLevels = sample
        if (targetSignalLevels == signalLevels):
            returnValue.append(coords)
    return returnValue


targetSignalLevels = [int(argv[i]) for i in range(1, 5)]
targetCoords = coordinate(targetSignalLevels)

print(targetCoords)
