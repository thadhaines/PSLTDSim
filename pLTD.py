"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)
#mirLoc = os.path.join(dirname, 'verification','microWecc','microWECC_loadStep01F.mir')
mirLoc = os.path.join(dirname, 'delme','kundurGenTrip2','kundurGenTrip22F.mir')
mirLoc = os.path.join(dirname, 'delme','kundurStep','kundurStep2F.mir')

mirLoc = os.path.join(dirname, 'delme','sixMachineStepBA','SixMachineStepBA4F.mir')
mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A0F.mir')
mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A1F.mir')
mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A1IACEF.mir')
mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A2IACEF.mir')

mir = ltd.data.readMirror(mirLoc)
ltd.terminal.dispSimTandC(mir)
xend = max(mir.r_t)
print(mir)

printFigs = False
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysVmVa(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.allPmDynamics(mir, False)

#ltd.plot.sysPLQF(mir, True)

# Plot ACE results
ltd.plot.BAplots01(mir, False)

### Plot detailed SACE
#Plot SACE from all areas on same plot
mins = np.array(mir.r_t)/60.0;
minEnd = max(mins)
caseName = mir.simParams['fileName'][:-1]
mini = 1

fig, ax = plt.subplots()
for BA in mir.BA:
    if BA.filter != None:
        ax.plot(mins, BA.r_ACEfilter, linewidth=1.25,linestyle=":",
                label= BA.name+' SACE')

# Scale current axis.
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.set_title('Balancing Authority SACE\n Case: ' + caseName)
ax.set_xlim(0,minEnd)
ax.set_ylabel('MW')
ax.set_xlabel('Time [minutes]')

#ax.legend(loc=0)
ax.grid(True)
fig.set_dpi(150)
fig.set_size_inches(9/mini, 2.5)
fig.tight_layout()
if printFigs: plt.savefig(caseName+'SACE'+'.pdf', dpi=300)
plt.show(block = False)
plt.pause(0.00001)

### Plot Area Change in Losses over time
mins = np.array(mir.r_t)/60.0;
minEnd = max(mins)
caseName = mir.simParams['fileName'][:-1]
mini = 1

fig, ax = plt.subplots()
for area in mir.Area:
    ax.plot(mins, np.array(area.r_Losses)-area.r_Losses[0], linewidth=1.25,#linestyle=":",
                label= 'Area '+ str(area.Area)+', Norm: '+ str(int(area.r_Losses[0])))

# Scale current axis.
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 1.05, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.set_title('Area Change in Losses\n Case: ' + caseName)
ax.set_xlim(0,minEnd)
ax.set_ylabel('MW')
ax.set_xlabel('Time [minutes]')

#ax.legend(loc=0)
ax.grid(True)
fig.set_dpi(150)
fig.set_size_inches(9/mini, 2.5)
fig.tight_layout()
if printFigs: plt.savefig(caseName+'Losses'+'.pdf', dpi=300)
plt.show()
plt.pause(0.00001)

"""
for gen in mir.Machines:
    print("%s    \t %f \t%f" %(gen.Busnam, gen.Hpu, gen.Mbase))

#Plot all dynamic responses from generators#
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
    # Plots max power line on dynamic plots
    ax[0].plot([mir.r_t[0], mir.r_t[-1]], [c_dyn.Gen.Pmax,c_dyn.Gen.Pmax], 
                #marker = '+',
                #linestyle = '--',
                label = 'Max Power')
    #

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

#ltd.plot.sysPemLQF(mir, True)

Plot governed generator log data
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