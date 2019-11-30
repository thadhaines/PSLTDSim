""" File to scan mirror for unused machines and governors,
additionaly, check for models that may have a 0.0 as a droop """

import os
import psltdsim as ltd
import time
global time

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
#os.chdir(r"D:\Users\jhaines\source\repos\thadhaines\PSLTDSim")
os.chdir(r"C:\Users\thad\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)

mirLoc = os.path.join( 'delme','fullWECC','fWECCstep.mir') # base case for AGC testing

print(mirLoc)
mir = ltd.data.readMirror(mirLoc)

print('debug stop...')

# Check for weird machines
mysteryGen = []
totGen = 0
foundGen = 0

for pmod in mir.PSLFmach:
    totGen +=1
    foundTest = ltd.find.findGenOnBus(mir, pmod.Busnum, pmod.Id)
    if foundTest == None:
        print('Gen not found: %d %s %s' %(pmod.Busnum, pmod.Busnam, pmod.Id))
        mysteryGen.append([pmod.Busnum, pmod.Busnam, pmod.Id])
    else:
        foundGen += 1

# Check for extra prime movers
mysteryPM = []
zeroRPM = []
totPM = 0
foundPM = 0
blankRdict = {}

for pmod in mir.PSLFgov:
    totPM += 1
    if pmod.Gen == None:
        print('PrimeMover has no associated generator: %d %s %s' %(pmod.Busnum, pmod.Busnam, pmod.Id))
        mysteryPM.append([pmod.Busnum, pmod.Busnam, pmod.Id])
    else:
        foundPM +=1 
        # check for blank R
        if pmod.R == 0.0:
            zeroRPM.append([pmod.Busnum, pmod.Busnam, pmod.Id, pmod.Type])
            if pmod.Type in blankRdict:
                blankRdict[pmod.Type][0] += 1
                blankRdict[pmod.Type][1].append(pmod.dydLine)
            else:
                blankRdict[pmod.Type] = [1, [pmod.dydLine]]


# outputs
print("Machine Stats...")
print("Found %d Good gens" % foundGen)
print("Found %d mystery gens" % len(mysteryGen))
print("out of %d total gens" % totGen)
print("Prime Mover Stats...")
print("Found %d Good prime movers" % foundPM)
print("Found %d mystery govs" % len(mysteryPM))
print("Found %d zero R govs" % len(zeroRPM))
print("out of %d total govs" % totPM)


''' Results:
Many models exist in the dyd that are no longer linked to PSLF objects.
Verified as the case for primemovers
Some machines are verified as missing in the .sav,  but not all (large number)

most blank Rs are associated with the hyg3 model
ggov1 models with blank R - some are isochronous, others are truly set to zero.
hyg3 has two spots for Rs - need to make some kind of routine to handle <- did this, seems to work- fixed 134 zero Rs

gpwscc is werid, but maybe is being parsed wrong?- no, models actually have zero droop...
'''

# print dyd line of zero R 
for key in blankRdict:
    for listedDydLine in blankRdict[key][1]:
        print(listedDydLine)


mirLoc = os.path.join( 'delme','fullWECC','fWECCstepF.mir') # base case for AGC testing

print(mirLoc)
mir = ltd.data.readMirror(mirLoc)
ltd.terminal.dispSimTandC(mir)

# do something with generator island information...

# Find global slack island (or assume it to be one)
gblIsland = 1
ignores = 0

for gen in mir.Machines:
    if gen.Bus.Islnum != gblIsland:
        ignores +=1
        gen.cv['IRPflag'] = False

# over 100 generators should be ignored / not in main island
"""
IRPflag can be used  to handle required changes to:
global H calculation
area Beta calculation
pacc dist
"""

"""
Other thought:
manualy load wecc case,
solve,
change one value,
attempt to solve again.
All via python - just to see if GE software can actually do it.
"""