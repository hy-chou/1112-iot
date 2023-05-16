from json import dumps, loads

import numpy as np

with open('./data.json') as f:
        lines = f.readline()
data = loads(lines)

testing = []

# # mid-way
# for i in range(len(data)):
#     for j in range(i+1, len(data)):
#         near = 0
#         for a in range(3):
#             if data[i][0][a] == data[j][0][a]:
#                 near += 1
#         if near == 2:
#             testing.append([
#                 np.mean([data[i][0], data[j][0]], axis=0).tolist(),
#                 np.mean([data[i][1], data[j][1]], axis=0).tolist()
#             ])

for _ in range(10):
    # noise
    for i in range(len(data)):
        coords = np.array(data[i][0]) + np.random.rand(3) - np.random.rand(3)
        testing.append([coords.tolist(), data[i][1]])

    # mid-way w/ noise
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            near = 0
            for a in range(3):
                if data[i][0][a] == data[j][0][a]:
                    near += 1
            if near == 2:
                coords = np.mean([data[i][0], data[j][0]], axis=0) + np.random.rand(3) - np.random.rand(3)
                sl = np.mean([data[i][1], data[j][1]], axis=0)
                testing.append([coords.tolist(), sl.tolist()])

print(dumps(testing))
