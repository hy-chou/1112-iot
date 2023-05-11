from sys import argv

targetAPs = [
    '00:11:32:9D:2B:30',
    '00:11:32:9D:30:3A',
    '00:11:32:AD:8C:82',
    '00:11:32:AD:8E:B7',
]


itext = argv[1]
otext = ''

cells = itext.split('Cell')[1:]
for cell in cells:
    l = cell.replace('\n', '').replace(' ', '')

    p = l.find('Address:') + 8
    if l[p:p+17] not in targetAPs:
        continue

    p = l.find('Signallevel:') + 12
    q = p + l[p:].find('dBm')

    otext += l[p:q] + '\n'

print(otext)
