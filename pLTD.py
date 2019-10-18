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

#mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A0F.mir')
#mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A1F.mir')
mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A1IACEF.mir')
#mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A2IACEF.mir')
#mirLoc = os.path.join(dirname, 'delme','sixMachineStep','SixMachineStep1F.mir')

# Deadband data
mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCnoDBF.mir')
mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCstepDBF.mir')
mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCNLdroopDBF.mir')

# IEEE testing
#mirLoc = os.path.join(dirname, 'delme','IEEE','3areaTripF.mir')
mirList = []

mirList.append(os.path.join(dirname, 'delme','IEEE','genTripHighRnoDBF.mir'))
mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRnoDBF.mir'))
mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRstepDBF.mir'))
mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRnonLinDBF.mir'))

mirLoc = os.path.join(dirname, 'delme','IEEE','miniWECCgenTripF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','genTripHighRnoDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','genTripEqualRnoDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','genTripEqualRstepDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','genTripEqualRnonLinDBF.mir')

#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windramp2F.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBFastF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBSlowF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBSlowGainF.mir')
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBFastGainF.mir') # Fast gain...
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBFastGainIACEF.mir') # Fast gain...
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBFastGainIACENoFilterF.mir') # Fast gain...
#mirLoc = os.path.join(dirname, 'delme','IEEE','windrampNoDBFastGainIACENoBF.mir') # Fast gain...

mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoiseF.mir') # 10 minutes of noise
mirLoc = os.path.join(dirname, 'delme','noiseTest','miniWECCnoiseF.mir') # 10 minutes of noise

mir = ltd.data.readMirror(mirLoc)
ltd.terminal.dispSimTandC(mir)
xend = max(mir.r_t)
print(mir)

printFigs =   False # True # 
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysVmVa(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.allPmDynamics(mir, False)

#ltd.plot.sysPLQF(mir, True)
#ltd.plot.ValveTravel(mir, False, printFigs)
ltd.plot.ValveTravel01(mir, False, printFigs)
#ltd.plot.BAplots01(mir, False, printFigs)
ltd.plot.sysF(mir, False, printFigs)

#ltd.plot.AreaLosses(mir,False, printFigs)
#ltd.plot.BAgovU(mir, False, printFigs)
ltd.plot.SACE(mir,False, printFigs)
ltd.plot.ACE2dist(mir, True, printFigs)
#ltd.plot.oneGenDynamics(mir, True, printFigs, 17) # 4th input is bus num of gen


# Plot loopy results
"""
printFigs = True
for case in mirList:
    mir = ltd.data.readMirror(case)
    ltd.terminal.dispSimTandC(mir)
    ltd.plot.ValveTravel(mir, False, printFigs)
    ltd.plot.BAplots01(mir, False, printFigs)
"""