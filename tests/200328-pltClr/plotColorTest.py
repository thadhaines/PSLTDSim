""" Experiemntation with alternative color cycle for use in plots """

import matplotlib.pyplot as plt
import numpy as np

from cycler import cycler

ltdColors=[ [0,0,0], # black
        [.7,.7,.7], # grey
        [0,1,0], # green
        [1,0,1], # magenta
        #[0,1,1], # cyan
        "#17becf", # light blue
        [1,.647,0],# orange
        #"#ff7f0e", #orange
    ]

ltdStyles =  ["-","--",':',"-","--",':'
        ]

default_cycler = (
     cycler(color=ltdColors)
    + cycler(linestyle=ltdStyles)
                 )

#plt.rc('lines', linewidth=4)
plt.rc('axes', prop_cycle=default_cycler)

nLines = 12
nPoints = 30

fig, ax = plt.subplots()

xData = range(0,nPoints)

for lines in range(0,nLines):
    yData = np.random.random(nPoints)
    ax.plot(xData, yData,
            label = str(lines)
                        )

ax.legend()
ax.grid(True)
fig.tight_layout()
plt.show(block = True)
plt.pause(0.00001)

"""
Result:
Using a cycler to alter the plt.rc axes prop cycle does the desired thing.
"""

# custom color cycler
from cycler import cycler
ltdColors=[ [0,0,0], # black
        [.7,.7,.7], # grey
        [0,1,0], # green
        [1,0,1], # magenta
        "#17becf", # light blue
        [1,.647,0],# orange
    ]
default_cycler = (cycler(color=ltdColors))
plt.rc('axes', prop_cycle=default_cycler)