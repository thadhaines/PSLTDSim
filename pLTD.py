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

#IEEE results 2 - non AGC 10/29/19
#mirList = []
#folderName = '191029-paperSimsNoAGC'
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCuniAccF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCatlAGCF.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir') # base case for AGC testing
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCuniAccF.mir'))

#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir'))
#mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNLdroopDBF.mir'))
#ltd.plot.sysFcomp(mirList,blkFlag=False, printFigs=True) # multiple mir comp

#mirLoc = os.path.join(dirname, 'delme','sixMachineRamp','sixMachineRamp1F.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenMach2F.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov1F.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov2F.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','191114-genericsTest','sixMachineStepGenGov3F.mir') # base case for AGC testing
#mirLoc = os.path.join(dirname, 'delme','genMW','genMWstepF.mir') # base case for AGC testing

# WECC data plot
#mirLoc = os.path.join(dirname, 'delme','fullWECC','fWECCstepF.mir') # base case for AGC testing

# load control
#mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRLF.mir') # load ctrl testing...
#mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRL2F.mir') # load ctrl testing...
#mirLoc = os.path.join(dirname, 'delme','sixMachineLoadCTRL','sixMachineLoadCTRL3F.mir') # load ctrl testing...
# gen control
#mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRLF.mir') # load ctrl testing...
#mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRL2F.mir') # load ctrl testing...
#mirLoc = os.path.join(dirname, 'delme','sixMachineGenCTRL','sixMachineGenCTRL3F.mir') # load ctrl testing...

# Retesting of ACE polts post RACE introduction
#mirLoc = os.path.join(dirname, 'delme','191029-paperSimsNoAGC','miniWECCnoiseNoDBF.mir')

# delay inspection
#mirLoc = os.path.join(dirname, 'delme','delayTest','SixMachineDelayStep1F.mir')
#mirLoc = os.path.join(dirname, 'delme','delayTest','SixMachineDelayStep2F.mir')
#mirLoc = os.path.join(dirname, 'delme','delayTest','SixMachineDelayStep3F.mir')

#delay scenario inspection
#mirLoc = os.path.join(dirname, 'delme','200109-delayScenario1','SixMachineDelayStep1F.mir') #AGC Tuning
#mirLoc = os.path.join(dirname, 'delme','200109-delayScenario1','SixMachineDelayStep2F.mir') # No AGC
#mirLoc = os.path.join(dirname, 'delme','200109-delayScenario1','SixMachineDelayStep3F.mir') # Delay, with AGC
#mirLoc = os.path.join(dirname, 'delme','200109-delayScenario1','SixMachineDelayStep4F.mir') # Delay No AGC
#mirLoc = os.path.join(dirname, 'delme','200109-delayScenario1','SixMachineDelayStep5F.mir') # Equal delay and non-delay gov response

#Thesis Validation mirrors...
#mirLoc = os.path.join(dirname, 'delme','thesisV','miniWECCrampF.mir') # load ctrl testing...

# Mini WECC delay Case
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep1F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep2F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep3F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep4F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep1AGCF.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep2AGCF.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep3AGCF.mir') 
#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep4AGCF.mir') 

#mirLoc = os.path.join(dirname, 'delme','200123-miniWECCdelay','miniWECCDelayStep5AGCF.mir') # swinging scenario

# Daily contol results.
#mirLoc = os.path.join(dirname, 'delme','200127-sixMachineDailyCTRL','sixMachineDailyCTRLF.mir') 

# Shunt Contorl Test
#mirLoc = os.path.join(dirname, 'delme','200131-ShuntControlDev','sixMachineShuntCTRLF.mir') 

# Sunset
#mirLoc = os.path.join(dirname, 'delme','200201-sunset','sixMachineSunsetF.mir') 
# windramp
#mirLoc = os.path.join(dirname, 'delme','200202-windramp','sixMachineWindrampF.mir') 

# DTC
#mirLoc = os.path.join(dirname, 'delme','200202-dtc','sixMachineDTCF.mir') 
# DTC windramp
#mirLoc = os.path.join(dirname, 'delme','200203-DTCwindramp','sixMachineWindramp1F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200203-DTCwindramp','sixMachineWindramp2F.mir') 
#mirLoc = os.path.join(dirname, 'delme','200203-DTCwindramp','sixMachineWindramp4F.mir') 
mirLoc = os.path.join(dirname, 'delme','200203-DTCwindramp','sixMachineWindramp5F.mir') #deadbands

# Automatable H
#mirLoc = os.path.join(dirname, 'delme','200203-Hpert','sixMachineHpertF.mir') 
#full WECC
mirLoc = os.path.join(dirname, 'delme','fullWECC','fWECCstepF.mir') #deadbands


mir = ltd.data.readMirror(mirLoc)
#ltd.terminal.dispSimTandC(mir)
xend = max(mir.r_t)
print(mir)
printFigs = False # True # 
#ltd.plot.sysPePmFLoad(mir, False, printFigs)
ltd.plot.sysPePmFLoad2(mir, False, printFigs)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysShuntV(mir, False, printFigs)
#ltd.plot.sysShuntMVAR(mir, False, printFigs)
#ltd.plot.sysShunt(mir, False, printFigs)
#ltd.plot.sysVmVa(mir, True)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPLQF(mir, False)

#ltd.plot.allPmDynamics(mir, False)

#ltd.plot.sysPLQF(mir, True)
#ltd.plot.ValveTravel(mir, False, printFigs) # per area, legend outside right
#ltd.plot.ValveTravel01(mir, True, printFigs) # all govs in one graph
ltd.plot.sysF(mir, False, printFigs)
ltd.plot.sysH(mir, False, printFigs)

#ltd.plot.BAplots01(mir, False, printFigs) # legend on outside of plot


#ltd.plot.BAplots02(mir, False, printFigs) # legend on inside of right plot

#ltd.plot.ValveTravel00(mir, False, printFigs) # per area, legend inside right
#ltd.plot.branchMVAR(mir, 8, [9], False, printFigs) # per area, legend inside right

ltd.plot.PloadIEEE(mir,True, printFigs=False, miniFlag = True)
#ltd.plot.AreaRunningValveTravel(mir,True, True)

#ltd.plot.AreaLosses(mir,True, printFigs)
#ltd.plot.BAgovU(mir, True, printFigs)
#ltd.plot.BAALtest(mir, True, printFigs)
#ltd.plot.SACE(mir,False, printFigs)
#ltd.plot.ACE2dist(mir, True, printFigs)
#ltd.plot.oneGenDynamics(mir, True, printFigs, 17) # 4th input is bus num of gen

#ltd.plot.sysFcomp(mirList,True, printFigs=False) # multiple mir comp

# Branch MW Flow
#ltd.plot.branchMW(mir, 8,9, True, printFigs) # for six machine delay scenario
#ltd.plot.branchMW2(mir, 89,[38,90,110], True, printFigs) # for miniWECC COI
#ltd.plot.branchMW(mir, 89, 110,  True, printFigs) # for miniWECC COI,
#ltd.plot.branchMW(mir, 89,38, True, printFigs) # for miniWECC COI
#ltd.plot.branchMW(mir, 110,108, True, printFigs) # branch post xfm
#ltd.plot.branchMW3(mir, 89,[38,90],110,[108], True, printFigs) # All COI connections



miniFlag = True
printFigs = True
#ltd.plot.AreaPLoad(mir, False, printFigs,miniFlag)
#ltd.plot.AreaPe(mir, True, printFigs,miniFlag)
#ltd.plot.AreaPm(mir, True, printFigs,miniFlag)

# Plot loopy results

#printFigs = True
#for case in mirList:
#    mir = ltd.data.readMirror(case)
#    ltd.terminal.dispSimTandC(mir)
#    ltd.plot.ValveTravel01(mir, False, printFigs, miniFlag = True)
#    ltd.plot.sysF(mir, False, printFigs)

#ltd.plot.genDynamicsComp(mirList, blkFlag=True, printFigs = True, genNum = 32)
