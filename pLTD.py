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

mir = ltd.data.readMirror(mirLoc)
ltd.terminal.dispSimTandC(mir)
xend = max(mir.r_t)
printFigs = False
#ltd.plot.sysPQVF(mir, 0)
#ltd.plot.sysPePmFLoad(mir, 1)
mini = 1 # rethink - use to scale width of figures

#xend = 60
caseName = mir.simParams['fileName'][:-1]
# Plot controlled machines Pref and Pm
for BA in mir.BA:
    fig, ax = plt.subplots()
    for gen in BA.ctrlMachines:
        ax.plot(mir.r_t, gen.r_Pm,linestyle = '-',linewidth=1,
                label = r'$P_m$  '+str(gen.Busnum)+' '+gen.Id  )
        ax.plot(mir.r_t, gen.r_Pref,linestyle = '--',linewidth=1.5,
                label = r'$P_{ref}$ '+str(gen.Busnum)+' '+gen.Id  )
        
    ax.set_title(r'Area '+str(gen.Area)+ ' Controlled Machines $P_m$ and $P_{ref}$')
    ax.set_xlim(0,xend)
    ax.set_ylabel('MW')
    ax.set_xlabel('Time [sec]')
    ax.legend(loc=5)
    ax.grid(True)
    fig.set_dpi(150)
    fig.set_size_inches(9/mini, 2.5)
    fig.tight_layout()
    plt.show(block=False)
    if printFigs: plt.savefig(caseName+BA.name+'.pdf', dpi=300)
    plt.pause(0.00001) # required for true non-blocking print...

#Plot Interchange Error and ACE on same plot
fig, ax = plt.subplots()
for BA in mir.BA:
    ax.plot(mir.r_t, BA.r_ACE, linewidth=1,
            label= BA.name+' ACE')
    if BA.filter != None:
        ax.plot(mir.r_t, BA.r_ACEfilter, linewidth=1.25,linestyle=":",
                label= BA.name+' SACE')
    ax.plot(mir.r_t, BA.Area.r_ICerror, linewidth=1.5,
            linestyle='--',
            label= BA.name +' IC Error')
ax.set_title('Balancing Authority ACE and Interchange Error')
ax.set_xlim(0,xend)
ax.set_ylabel('MW')
ax.set_xlabel('Time [sec]')
ax.legend(loc=10)
ax.grid(True)
fig.set_dpi(150)
fig.set_size_inches(9/mini, 2.5)
fig.tight_layout()
plt.show(block=False)
if printFigs: plt.savefig(caseName+'ACE'+'.pdf', dpi=300)
plt.pause(0.00001)

#Plot System Frequency
fig, ax = plt.subplots()
fig.set_size_inches(6, 2)
ax.plot(mir.r_t, np.array(mir.r_f)*60.0,linewidth=1,)
ax.set_title('System Frequency')
ax.set_ylabel('Hz')
ax.set_xlabel('Time [sec]')
ax.set_xlim(0,xend)
#ax.legend()
ax.grid(True)
fig.set_dpi(150)
fig.set_size_inches(9/mini, 2.5)
fig.tight_layout()
if printFigs: plt.savefig(caseName+'Freq'+'.pdf', dpi=300)
plt.show()
plt.pause(0.00001)

print(mir)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysVmVa(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.allPmDynamics(mir, False)


# Plot ACE results

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