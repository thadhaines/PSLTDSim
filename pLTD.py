"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)
mirLoc = os.path.join(dirname, 'verification','refactor','ramp02F.mir')
mir = ltd.data.readMirror(mirLoc)
simParams = {'fileName':'turd',
             'fileDirectory' : None,
             }
ltd.data.exportMat(mir, simParams)

xend = max(mir.r_t)

print(mir)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.sysPQgen(mir, False)
#ltd.plot.sysPQVF(mir, False)

ltd.plot.sysVmVa(mir)


"""Plot system P and Q of active loading

fig, ax = plt.subplots(nrows=2, ncols=1,)
ax[0].set_title('System P Load')
ax[1].set_title('System Q Load')
for load in mir.Load:
    ax[0].plot(mir.r_t, np.array(load.r_P)*np.array(load.r_St), 
                marker = 10,
                linestyle = ':',
                label = 'Bus '+ load.Bus.Busnam +' Id ' + load.Id)
    ax[1].plot(mir.r_t, np.array(load.r_Q)*np.array(load.r_St), 
                marker = 'o',
                linestyle = ':',
                label = 'Bus '+ load.Bus.Busnam +' Id ' + load.Id)
ax[0].set_xlabel('Time [sec]')
ax[0].set_ylabel('MW')
ax[1].set_xlabel('Time [sec]')
ax[1].set_ylabel('MVAR')

# Global Plot settings
for x in np.ndarray.flatten(ax):
    x.set_xlim(0,xend)
    x.legend()
    x.grid(True)

fig.tight_layout()

plt.show()
"""