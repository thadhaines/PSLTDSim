"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)
mirLoc = os.path.join(dirname, 'verification','refactor','ramp','tGovRamp01F.mir')
mir = ltd.data.readMirror(mirLoc)

xend = max(mir.r_t)

print(mir)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysPePmF(mir, False)
ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)

ltd.plot.sysPQgen(mir, False)
#ltd.plot.sysPQVF(mir, False)

#ltd.plot.sysVmVa(mir, False)


"""Plot system Pacc and Freq"""

fig, ax = plt.subplots(nrows=3, ncols=1,)
ax[0].set_title('System Pacc')
ax[1].set_title('Governed Generator Power Output')
ax[2].set_title('Governor States')
ax[0].plot(mir.r_t, mir.r_ss_Pacc, 
            marker = 10,
            linestyle = ':',
            label = 'Pacc')

ax[1].plot(mir.r_t, mir.Dynamics[0].Gen.r_Pe, 
            marker = 'o',
            #markerfill = 'None',
            linestyle = ':',
            label = 'Pe')
ax[1].plot(mir.r_t, mir.Dynamics[0].Gen.r_Pm, 
            marker = '+',
            linestyle = '--',
            label = 'Pm')

ax[2].plot(mir.r_t, mir.Dynamics[0].r_x1, 
            marker = '1',
            linestyle = '--',
            label = 'x1')
ax[2].plot(mir.r_t, mir.Dynamics[0].r_x2, 
            marker = '2',
            linestyle = ':',
            label = 'x2')
ax[0].set_xlabel('Time [sec]')
ax[0].set_ylabel('MW')
ax[1].set_xlabel('Time [sec]')
ax[2].set_xlabel('Time [sec]')
ax[1].set_ylabel('PU')
ax[2].set_ylabel('State')
# Global Plot settings
for x in np.ndarray.flatten(ax):
    x.set_xlim(0,xend)
    x.legend()
    x.grid(True)

fig.tight_layout()

plt.show()
