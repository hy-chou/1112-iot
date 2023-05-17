
import matplotlib.pyplot as plt
import numpy as np


table = [
    [8.008224462802675 , 13535.219384900709],
    [8.052425440559091 , 11129.566180842046],
    [8.066864701046487 , 10473.856114404902],
    [8.08031625495441  , 10185.549009115484],
    [8.090972263335642 , 10002.772982776156],
    [8.100615904410352 , 9896.949047983464],
    [8.109607082891724 , 9829.069393061905],
    [8.117636941411272 , 9797.285404514354],
    [8.124127030273952 , 9796.356944747487],
    [8.13000091488268  , 9809.310843766778],
    [8.136698630860305 , 9821.53634204924],
    [8.14212191527468  , 9830.390335141954],
    [8.146757320816254 , 9837.696548763732],
    [8.151735495772614 , 9851.823526259104],
    [8.156115498482297 , 9889.116190712153],
    [8.160620889559425 , 9907.033809657314],
    [8.164605688321123 , 9911.5213878222],
    [8.168815936077099 , 9921.428945510306],
    [8.173258406118087 , 9940.496564602185],
    [8.177371626346575 , 9950.354271012433],
    [8.181107230247212 , 9950.818883188464],
    [8.184278764065928 , 9976.776522501737],
    [8.187077324470689 , 9989.359514085283],
    [8.190449523991727 , 9987.443613826232],
    [8.193249984728043 , 9983.785904943024],
    [8.195817283697757 , 9980.146270463316]
]

samples = [i[0] / 109 for i in table]
testing = [i[1] / 7500 for i in table]

x = range(1, 27)

fig, ax = plt.subplots()

ax.plot(x, samples, x, testing)

ax.set_ylabel('error (1 unit = 0.6 meter)')
ax.set_xlabel('k value')
ax.legend(['sample', 'testing'])

plt.savefig(f'tmp.png', bbox_inches='tight')
plt.close(fig)