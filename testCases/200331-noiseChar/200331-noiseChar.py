"""
The ability to generate noise behavior without running a simulation may be helpful in choosing random seed values that produce certain pre-defined system responses.
As all computers only do pseudo random number gen - this should be possilbe
can only do relative changes per load.... maybe good enough to be useful?
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import psltdsim as ltd

dirname = os.path.dirname(__file__)
tempFolder = os.path.split(dirname)[0]
dirname = os.path.split(tempFolder)[0] # root git folder

mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTfdDBnzF.mir') # forcast demand with nz
mir = ltd.data.readMirror(mirLoc)

class GenObj():
    def __init__(self, name):
        self.name = str(name)

rSeed = 11
pNoise = 0.05 # perent of noise to add
delay = 1

timeStep = 1 # seconds
simTime = 60*10 # seconds

numArea = 2
numAreaLoad = [1,1] # number of loads per area

# create time vector
dps = int(simTime/timeStep)
t = [0.0]*dps

# create running value lists for each load
areaList = []
for areaNum in range(numArea):
    newArea = GenObj(areaNum)
    newArea.loadList = []
    for loadNum in range(numAreaLoad[areaNum]):
        newLoad = GenObj("A"+str(areaNum)+"L"+str(loadNum))
        newLoad.val = [1.0]*dps # all loads init at 1
        newArea.loadList.append(newLoad)
    areaList.append(newArea)

## Alternative method: create loads from mirror....
loadList = []
for load in mir.Load:
    newLoad = GenObj(load)
    newLoad.val = [load.cv['P']]*dps
    loadList.append(newLoad)

# seed random number generator
np.random.seed(rSeed)
# scale percnoise 
pNoise = pNoise/100.00

# for each time step
for step in range(dps):
    t[step] = step*timeStep

    if t[step] < delay:
        continue
    """
    # for each area
    for area in areaList:

        # for each load
        for load in area.loadList:
            # choose sign
            if np.random.randint(2): # returns a 1 or 0
                #subtract
                noise = -pNoise*np.random.ranf()
            else:
                #add
                noise = pNoise*np.random.ranf()

            # add to load
            seedVal = load.val[step-1] # get load val
            newVal = round(seedVal*(1.0 + noise),4) # same behavior as noise agent
            load.val[step] = newVal
    """
    for load in loadList:
    # choose sign
        if np.random.randint(2): # returns a 1 or 0
            #subtract
            noise = -pNoise*np.random.ranf()
        else:
            #add
            noise = pNoise*np.random.ranf()

        # add to load
        seedVal = load.val[step-1] # get load val
        newVal = round(seedVal*(1.0 + noise),4) # same behavior as noise agent
        load.val[step] = newVal

""" plot outputs """
fig, ax = plt.subplots()
"""
for area in areaList:
    areaTot = [0.0]*dps

    for load in area.loadList:
        areaTot += np.array(load.val)
        ax.plot(t, load.val, label=load.name, linestyle="--", linewidth=.75)
    ax.plot(t, areaTot/len(area.loadList), label=area.name+" Total")
"""
for load in loadList:
    ax.plot(t, np.array(load.val)-load.val[0], label=load.name, linestyle="--", linewidth=.75)

ax.set_title('Change in System Loading')
ax.set_xlim(0,max(t))
ax.set_ylabel('% change')
ax.set_xlabel('Time [seconds]')
ax.legend()

#ax.legend(loc=0)
ax.grid(True)
#fig.set_dpi(150)
#fig.set_size_inches(9, 2.5) 

fig.tight_layout()
#if printFigs: plt.savefig(caseName+'PloadChange'+'.pdf', dpi=300)
plt.show(block = True)
plt.pause(0.00001)

"""
Results:
Code does desired random generation... 
however without load scaling and the results are less than helpful

edit:
loading a mirror and collecting values from that can reproduce noise behavior.

"""