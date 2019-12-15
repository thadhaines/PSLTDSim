"""Generic plotting for function generation"""
import os
import matplotlib.pyplot as plt
import numpy as np

import psltdsim as ltd

#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")

dirname = os.path.dirname(__file__)

#mirLoc = os.path.join(dirname, 'verification','microWecc','microWECC_loadStep01F.mir')
#mirLoc = os.path.join(dirname, 'delme','kundurGenTrip2','kundurGenTrip22F.mir')
#mirLoc = os.path.join(dirname, 'delme','kundurStep','kundurStep2F.mir')

#mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A0F.mir')
#mirLoc = os.path.join(dirname, 'delme','miniWECC3A','miniWECC3A1F.mir')
#mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A1IACEF.mir')
#mirLoc = os.path.join(dirname, 'delme','BA2','miniWECC3A2IACEF.mir')
#mirLoc = os.path.join(dirname, 'delme','sixMachineStep','SixMachineStep1F.mir')

# Deadband data
#mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCnoDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCstepDBF.mir')
#mirLoc = os.path.join(dirname, 'delme','BA3','miniWECCNLdroopDBF.mir')

# IEEE testing
#mirLoc = os.path.join(dirname, 'delme','IEEE','3areaTripF.mir')
#mirList = []

#mirList.append(os.path.join(dirname, 'delme','IEEE','genTripHighRnoDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRnoDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRstepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','IEEE','genTripEqualRnonLinDBF.mir'))

#mirLoc = os.path.join(dirname, 'delme','IEEE','miniWECCgenTripF.mir')
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

#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoiseF.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoise2F.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoise3F.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoise4F.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoise5F.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','sixMachineNoise','SixMachineNoiseXF.mir') # 10 minutes of noise

#mirLoc = os.path.join(dirname, 'delme','noiseTest','miniWECCnoiseNoDBF.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','noiseTest','miniWECCnoiseNLDBF.mir') # 10 minutes of noise
#mirLoc = os.path.join(dirname, 'delme','noiseTest','miniWECCnoiseStepDBF.mir') # 10 minutes of noise


#mirLoc = os.path.join(dirname, 'delme','191023-db','mwBASEF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191023-db','mw10NoDBAGCF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191023-db','mw05NoDBAGCF.mir') # base case for AGC testing

#mirList = []
# Second time step
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NoDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10StepDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NoStepDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NLdroopDBAGCF.mir'))
#ltd.plot.sysFcomp(mirList,blkFlag=False, printFigs=False) # multiple mir comp

#mirList = []
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NoDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10StepDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NoStepDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw10NLdroopDBNoAGCF.mir'))
#ltd.plot.sysFcomp(mirList,blkFlag=False, printFigs=False) # multiple mir comp

#mirList = []
# Half Second time step
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NLdroopDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NoDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05StepDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NoStepDBAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NLdroopDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NoDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05StepDBNoAGCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191023-db','mw05NoStepDBNoAGCF.mir'))

#IEEE results
#mirList = []
#mirLoc = os.path.join(dirname, 'delme','191028-paperSims','miniWECCnoiseNoDBF.mir') # base case for AGC testing
#mirList.append(os.path.join(dirname, 'delme','191028-paperSims','miniWECCnoiseNoDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191028-paperSims','miniWECCnoiseStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191028-paperSims','miniWECCnoiseNoStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme','191028-paperSims','miniWECCnoiseNLdroopDBF.mir'))
#ltd.plot.sysFcomp(mirList,blkFlag=True, printFigs=False) # multiple mir comp

printFigs =    False # True #


#IEEE results 2 - non AGC 10/29/19
mirList = []
folderName = '191029-paperSimsNoAGC'
mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCuniAccF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCatlAGCF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir') # base case for AGC testing
mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCuniAccF.mir'))

#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNLdroopDBF.mir'))
#ltd.plot.sysFcomp(mirList,blkFlag=False, printFigs=True) # multiple mir comp


mirLoc = os.path.join(dirname, 'delme','sixMachineRamp','sixMachineRamp1F.mir') # base case for AGC testing
mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenMach2F.mir') # base case for AGC testing
mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov1F.mir') # base case for AGC testing
mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov2F.mir') # base case for AGC testing
mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov3F.mir') # base case for AGC testing
mirLoc = os.path.join(dirname, 'delme','genMW','genMWstepF.mir') # base case for AGC testing

# WECC data plot
mirLoc = os.path.join(dirname, 'delme','fullWECC','fWECCstepF.mir') # base case for AGC testing

# load control
mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRLF.mir') # load ctrl testing...
mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRL2F.mir') # load ctrl testing...
mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRL3F.mir') # load ctrl testing...
# gen control
mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRLF.mir') # load ctrl testing...
mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRL2F.mir') # load ctrl testing...
mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRL3F.mir') # load ctrl testing...

mir = ltd.data.readMirror(mirLoc)
#ltd.terminal.dispSimTandC(mir)
xend = max(mir.r_t)
print(mir)

#ltd.plot.sysLoad(mir, True)
#ltd.plot.sysVmVa(mir, False)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPePmFLoad(mir, False)
ltd.plot.sysPLQF(mir, False)

#ltd.plot.allPmDynamics(mir, False)

#ltd.plot.sysPLQF(mir, True)
#ltd.plot.ValveTravel(mir, False, printFigs)
#ltd.plot.ValveTravel01(mir, True, printFigs)
#ltd.plot.BAplots01(mir, True, printFigs=False)
ltd.plot.sysF(mir, True, printFigs)

ltd.plot.PloadIEEE(mir,True, printFigs=False, miniFlag = True)
#ltd.plot.AreaRunningValveTravel(mir,True, True)

#ltd.plot.AreaLosses(mir,True, printFigs)
#ltd.plot.BAgovU(mir, False, printFigs)
#ltd.plot.SACE(mir,False, printFigs)
#ltd.plot.ACE2dist(mir, True, printFigs)
#ltd.plot.oneGenDynamics(mir, True, printFigs, 17) # 4th input is bus num of gen

#ltd.plot.sysFcomp(mirList,True, printFigs=False) # multiple mir comp

# Plot loopy results

#printFigs = True
#for case in mirList:
#    mir = ltd.data.readMirror(case)
#    ltd.terminal.dispSimTandC(mir)
#    ltd.plot.ValveTravel01(mir, False, printFigs, miniFlag = True)
#    ltd.plot.sysF(mir, False, printFigs)

#ltd.plot.genDynamicsComp(mirList, blkFlag=True, printFigs = True, genNum = 32)
