"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)
mirLoc = os.path.join(dirname, 'verification','refactor','tgov_steps','stepsTgov101F.mir')
mir = ltd.data.readMirror(mirLoc)

xend = max(mir.r_t)

print(mir)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.sysPQgen(mir, False)
#ltd.plot.sysPQVF(mir, False)

#ltd.plot.sysVmVa(mir)


"""Plot system Pacc and Freq"""

fig, ax = plt.subplots(nrows=2, ncols=1,)
ax[0].set_title('Pacc')
ax[1].set_title('System f')
ax[0].plot(mir.r_t, mir.r_ss_Pacc, 
            marker = 10,
            linestyle = ':',
            label = 'Pacc')
ax[1].plot(mir.r_t, mir.r_f, 
            marker = 'o',
            linestyle = ':',
            label = 'f')
ax[0].set_xlabel('Time [sec]')
ax[0].set_ylabel('MW')
ax[1].set_xlabel('Time [sec]')
ax[1].set_ylabel('PU')

# Global Plot settings
for x in np.ndarray.flatten(ax):
    x.set_xlim(0,xend)
    x.legend()
    x.grid(True)

fig.tight_layout()

plt.show()
