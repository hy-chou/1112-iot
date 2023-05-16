from json import dumps
from os import listdir


apMACs = [
    '00:11:32:9D:2B:30',
    '00:11:32:9D:30:3A',
    '00:11:32:AD:8C:82',
    '00:11:32:AD:8E:B7',
]

data = []

files = listdir('./data')
for file in files:
    coords = [int(r) for r in file[:-4].split('-')]

    sl = [-99, -99, -99, -99]

    with open(f'./data/{file}') as f:
        lines = f.readlines()
    for line in lines:
        if not line.startswith('00:11:32'):
            continue

        mac = line[:17]
        macID = apMACs.index(mac)

        p = line.find('Signallevel=') + 12
        signalLevel = int(line[p:-1])

        # select the strongest signal level for each AP
        if signalLevel > sl[macID]:
            sl[macID] = signalLevel

    data.append([coords, sl])

print(dumps(data))
