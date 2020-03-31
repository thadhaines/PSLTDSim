""" 4 hour sim used in thesis noise separation"""

import os
import matplotlib.pyplot as plt
import numpy as np
import psltdsim as ltd


dirname = os.path.dirname(__file__)
tempFolder = os.path.split(dirname)[0]
dirname = os.path.split(tempFolder)[0] # root git folder

printFigs = True
mirList = []
mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTfdF.mir') # forcast demand ideal
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTfdDBnzF.mir') # forcast demand with nz
mirList.append( mirLoc )


mir = ltd.data.readMirror(mirList[0])
mirNZ = ltd.data.readMirror(mirList[1])

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

mins = np.array(mir.r_t)/60.0;
minEnd = max(mins)
caseName = mir.simParams['fileName'][:-1]

fig, ax = plt.subplots()

nzP =  np.array(mirNZ.r_ss_Pload)
P = np.array(mir.r_ss_Pload)
ax.plot(mins, nzP-P, label="System Total")


nzP =  np.array(mirNZ.Area[0].r_P)
P = np.array(mir.Area[0].r_P)
ax.plot(mins, nzP-P, label="Area 1",linewidth=.85, linestyle="--")

nzP =  np.array(mirNZ.Area[1].r_P)
P = np.array(mir.Area[1].r_P)
ax.plot(mins, nzP-P, label="Area 2",linewidth=.85, linestyle="--")

#ax.plot(mins, P, label="load")
#ax.plot(mins, nzP, label="noise")


"""
ax.plot(mins, np.array(mirNZ.r_ss_Pload)-np.array(mir.r_ss_Pload), linewidth=1.0, 
        #color='black',
        label = 'System Total')

for area, areaNZ in mir.Area, mirNZ.Area:
    ax.plot(mins, np.array(area.r_P)-np.array(areaNZ.r_P), 
            linewidth=.85,
            linestyle="--",
            label = 'Area '+ str(area.Area)
            )
"""

ax.set_title('Change in System Loading')
ax.set_xlim(0,minEnd)
ax.set_ylabel('MW')
ax.set_xlabel('Time [minutes]')
ax.legend()

#ax.legend(loc=0)
ax.grid(True)
fig.set_dpi(150)
fig.set_size_inches(9, 2.5) 

fig.tight_layout()
if printFigs: plt.savefig(caseName+'PloadChange'+'.pdf', dpi=300)
plt.show(block = True)
plt.pause(0.00001)

ltd.plot.BAALtest(mirNZ)