"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)
mirLoc = os.path.join(dirname, 'verification','microWecc','microWECC_loadStep01F.mir')
mirLoc = os.path.join(dirname, 'verification','miniWeccTest01','miniWECC_loadStep06F.mir')
mir = ltd.data.readMirror(mirLoc)

xend = max(mir.r_t)

print(mir)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysPePmF(mir, False)
ltd.plot.sysPePmFLoad(mir, True)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.sysPQgen(mir, False)
#ltd.plot.sysPQVF(mir, True)

#ltd.plot.sysVmVa(mir, True)

for gen in mir.Machines:
    print("%s    \t %f \t%f" %(gen.Busnam, gen.Hpu, gen.Mbase))

""" Plot all dynamic responses from generators
for c_dyn in mir.Dynamics:
    fig, ax = plt.subplots(nrows=2, ncols=1,)
    ax[0].set_title('Governed Generator on Bus %d %s Power Output' 
                    % (c_dyn.Busnum, c_dyn.Busnam,))
    ax[1].set_title('Governor States')

    ax[0].plot(mir.r_t, c_dyn.Gen.r_Pe, 
                marker = 'o',
                #markerfill = 'None',
                linestyle = ':',
                label = 'Pe')
    ax[0].plot(mir.r_t, c_dyn.Gen.r_Pm, 
                marker = '+',
                linestyle = '--',
                label = 'Pm')

    ax[1].plot(mir.r_t, c_dyn.r_x1, 
                marker = '1',
                linestyle = '--',
                label = 'x1')
    ax[1].plot(mir.r_t, c_dyn.r_x2, 
                marker = '2',
                linestyle = ':',
                label = 'x2')

    ax[0].set_xlabel('Time [sec]')
    ax[1].set_xlabel('Time [sec]')
    ax[0].set_ylabel('MW')
    ax[1].set_ylabel('State')
    # Global Plot settings
    for x in np.ndarray.flatten(ax):
        x.set_xlim(0,xend)
        x.legend()
        x.grid(True)

    fig.tight_layout()

    plt.show(block = False)

ltd.plot.sysPLQF(mir)
"""

"""Plot governed generator log data
c_dyn = 1 # used as placeholder for function input

fig, ax = plt.subplots(nrows=2, ncols=1,)
ax[0].set_title('Governed Generator on Bus %d %s Power Output' 
                % (mir.Dynamics[c_dyn].Busnum, mir.Dynamics[c_dyn].Busnam,))
ax[1].set_title('Governor States')

ax[0].plot(mir.r_t, mir.Dynamics[c_dyn].Gen.r_Pe, 
            marker = 'o',
            #markerfill = 'None',
            linestyle = ':',
            label = 'Pe')
ax[0].plot(mir.r_t, mir.Dynamics[c_dyn].Gen.r_Pm, 
            marker = '+',
            linestyle = '--',
            label = 'Pm')

ax[1].plot(mir.r_t, mir.Dynamics[c_dyn].r_x1, 
            marker = '1',
            linestyle = '--',
            label = 'x1')
ax[1].plot(mir.r_t, mir.Dynamics[c_dyn].r_x2, 
            marker = '2',
            linestyle = ':',
            label = 'x2')

ax[0].set_xlabel('Time [sec]')
ax[1].set_xlabel('Time [sec]')
ax[0].set_ylabel('MW')
ax[1].set_ylabel('State')
# Global Plot settings
for x in np.ndarray.flatten(ax):
    x.set_xlim(0,xend)
    x.legend()
    x.grid(True)

fig.tight_layout()

plt.show()
"""