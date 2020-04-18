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
#mirLoc = os.path.join(dirname, 'delme','200203-DTCwindramp','sixMachineWindramp5F.mir') #deadbands

# Automatable H
#mirLoc = os.path.join(dirname, 'delme','200203-Hpert','sixMachineHpertF.mir') 

#full WECC
#mirLoc = os.path.join(dirname, 'delme','fullWECC','fWECCstepF.mir') #deadbands
#mirLoc = os.path.join(dirname, 'delme','thesisV','18HSPweccStepF.mir') #wecc step 2018
#mirLoc = os.path.join(dirname, 'delme','thesisV','18HSPweccRampF.mir') #wecc step 2018

# Q limit testing
#mirLoc = os.path.join(dirname, 'delme','200210-Qlim','sixMachineQlimF.mir') 

# Varibable Frequency Bias
#mirLoc = os.path.join(dirname, 'delme','200301-VariFreqB','sixMachineVariB1F.mir') #wecc step 2018

# Thesis AGC testing..
#mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCt3In1F.mir') #wecc step 2018

"""
Plot Functions
"""

#mir = ltd.data.readMirror(mirLoc)
#ltd.terminal.dispSimTandC(mir)

#xend = max(mir.r_t)
#print(mir)
#printFigs =  False #True 
#ltd.plot.sysPePmFLoad(mir, False,)
#ltd.plot.sysPePmFLoad2(mir, False, printFigs)
#ltd.plot.sysLoad(mir, False)
#ltd.plot.sysShuntV(mir, False, printFigs)
#ltd.plot.sysShuntMVAR(mir, False, printFigs)
#ltd.plot.sysShunt(mir, False, printFigs)
#ltd.plot.sysVmVa(mir, False)
#ltd.plot.sysVmVAR(mir, True)
#ltd.plot.sysPePmF(mir, False)
#ltd.plot.sysPLQF(mir, True)

#ltd.plot.allPmDynamics(mir, False)

#ltd.plot.sysPLQF(mir, True)
#ltd.plot.ValveTravel(mir, False, printFigs) # per area, legend outside right
#ltd.plot.ValveTravel01(mir, False, printFigs) # all govs in one graph
#ltd.plot.sysF(mir, True, printFigs)

#ltd.plot.BAplots01(mir, False, printFigs) # legend on outside of plot

#ltd.plot.sysH(mir, True, printFigs)

#ltd.plot.BAplots02(mir, False, printFigs) # legend on inside of right plot

#ltd.plot.ValveTravel00(mir, False, printFigs) # per area, legend inside right
#ltd.plot.branchMVAR(mir, 8, [9], False, printFigs) # per area, legend inside right


#ltd.plot.AreaLosses(mir,True, printFigs)
#ltd.plot.BAgovU(mir, True, printFigs)
#ltd.plot.BAALtest(mir, True, printFigs)
#ltd.plot.SACE(mir,False, printFigs)
#ltd.plot.ACE2dist(mir, True, printFigs)
#ltd.plot.oneGenDynamics(mir, True, printFigs, 17) # 4th input is bus num of gen

# list stuff...
#mirList = []
#printFigs = False
#mirList.append(os.path.join(dirname, 'delme','200220-govDTC','sixMachineGovNoDTCF.mir'))
#mirList.append(os.path.join(dirname, 'delme','200220-govDTC','sixMachineGovDTCF.mir'))

#mirList.append(os.path.join(dirname, 'delme','200301-VariFreqB','sixMachineVariB0F.mir'))
#mirList.append(os.path.join(dirname, 'delme','200301-VariFreqB','sixMachineVariB1F.mir'))

#ltd.plot.sysFcomp2(mirList,blkFlag=True, printFigs=printFigs) # multiple mir comp
#ltd.plot.sysPgenComp(mirList, 2, blkFlag=False, printFigs=False, ) # multiple mir comp of pe
#ltd.plot.sysPmComp(mirList, 2, blkFlag=False, printFigs=printFigs, ) # multiple mir comp of pe
#ltd.plot.sysPeComp(mirList, 2, blkFlag=True, printFigs=printFigs, ) # multiple mir comp of pe


# Branch MW Flow
#ltd.plot.branchMW(mir, 8,9, True, printFigs) # for six machine delay scenario
#ltd.plot.branchMW2(mir, 89,[38,90,110], True, printFigs) # for miniWECC COI
#ltd.plot.branchMW(mir, 89, 110,  True, printFigs) # for miniWECC COI,
#ltd.plot.branchMW(mir, 89,38, True, printFigs) # for miniWECC COI
#ltd.plot.branchMW(mir, 110,108, True, printFigs) # branch post xfm
#ltd.plot.branchMW3(mir, 89,[38,90],110,[108], True, printFigs) # All COI connections

#ltd.plot.AreaPLoad(mir, False, printFigs,miniFlag)
#ltd.plot.AreaPe(mir, True, printFigs,miniFlag)
#ltd.plot.AreaPm(mir, True, printFigs,miniFlag)


#================================================================================================
#================================================================================================
""" System Damping """
mirList = []
printFigs = True
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smD0F.mir'))
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smDposF.mir'))
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smDnegF.mir'))

#ltd.plot.sysFcomp2(mirList,blkFlag=True, printFigs=printFigs) # multiple mir comp

#================================================================================================
""" dtc gov step ff """
# list stuff...
mirList = []
printFigs = False
mirList.append(os.path.join(dirname, 'delme','200220-govDTC','sixMachineGovNoDTCF.mir'))
mirList.append(os.path.join(dirname, 'delme','200220-govDTC','sixMachineGovDTCF.mir'))

#ltd.plot.sysFcomp2(mirList,blkFlag=True, printFigs=printFigs) # multiple mir comp
#ltd.plot.sysPeComp(mirList, 2, blkFlag=True, printFigs=printFigs, ) # multiple mir comp of pe

#================================================================================================
""" Inertia sim changes"""
mirList = []
printFigs = True
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smH100F.mir'))
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smH90F.mir'))
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smH80F.mir'))
mirList.append(os.path.join(dirname, 'delme','200329-DandH','smH70F.mir'))

#ltd.plot.sysFcomp2(mirList,blkFlag=True, printFigs=printFigs) # multiple mir comp
#ltd.plot.genDynamicsComp2(mirList, blkFlag=True, printFigs = True, genNum = 1) # comparison of valve travel


""" Automatable H """
mirLoc = os.path.join(dirname, 'delme','200203-Hpert','sixMachineHpertF.mir') 
mir = ltd.data.readMirror(mirLoc)
#ltd.plot.sysH(mir, False, printFigs)
#ltd.plot.sysF(mir, False, printFigs)


#================================================================================================

""" Thesis deadband noise plots """
#IEEE results 2 - non AGC 10/29/19 - used in Deadband graphs
folderName = '191029-paperSimsNoAGC'
#mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir') # ramp / no step for uni test
mirLoc = os.path.join(dirname, 'delme',folderName,'miniWECCuniAccF.mir') # area 3 has larger deadband
mir = ltd.data.readMirror(mirLoc)

#ltd.plot.AreaRunningValveTravel(mir,True, True) # per area, 
#ltd.plot.ValveTravel(mir, False, True)

# List of test cases
mirList = []
mirList.append(mirLoc)
mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoDBF.mir'))
mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseStepDBF.mir'))
mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNoStepDBF.mir'))
mirList.append(os.path.join(dirname, 'delme',folderName,'miniWECCnoiseNLdroopDBF.mir'))

#ltd.plot.sysFcomp(mirList,blkFlag=True, printFigs=True) # multiple mir comp
#ltd.plot.genDynamicsComp(mirList, blkFlag=True, printFigs = True, genNum = 32) # comparison of valve travel
#ltd.plot.PloadIEEE2(mir,True, printFigs=True, miniFlag = False)

# Plot loopy results
#printFigs = True
#for case in mirList:
    #mir = ltd.data.readMirror(case)
    #ltd.plot.ValveTravel(mir, False, printFigs)

# BAAL testing
#mir = ltd.data.readMirror(mirList[1])
#ltd.plot.BAALtest(mir)

#================================================================================================
""" Thesis AGC Tuning plots """
mirList = []
baseCases = []
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCt4In1F.mir') # Condidtional ACE internal
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCt0In1F.mir') # Non Conditional ACE
mirList.append( mirLoc )

mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCt4Ex1F.mir') # Condidtional ACE External
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCt0Ex1F.mir') # Non Conditional ACE
mirList.append( mirLoc )

mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCtune1F.mir') # AGC Tune
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCtune2F.mir') #
mirList.append( mirLoc )

mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCdbnz1F.mir') # AGC noise
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCdbnz2F.mir') # AGC noise
mirList.append( mirLoc ) 

mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCbase1F.mir') # AGC base case 1 odd stuff via multibus gen?
mirList.append( mirLoc )
baseCases.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200325-smFinal','smAGCbase2F.mir') # AGC base case 2
mirList.append( mirLoc )
baseCases.append( mirLoc )

# BAAL testing
#mir = ltd.data.readMirror(mirList[1])
#ltd.plot.BAALtest(mir, True, True)

#ltd.plot.sysFcomp2(baseCases, True, True)

#for case in mirList:
    #mir = ltd.data.readMirror(case)
    #print(mir)

#mir = ltd.data.readMirror(mirList[6])
#ltd.plot.PloadIEEE2(mir,True, printFigs=True, miniFlag = False)

#ltd.plot.sysFcomp(mirList,blkFlag=True, printFigs=False) # multiple mir comp
#ltd.plot.sysF(mir, True, False) # single frequency plot
#ltd.plot.BAplots02(mir, False)
##ltd.plot.PloadIEEE(mir,True, printFigs=False, miniFlag = False)


#for case in mirList:
    #mir = ltd.data.readMirror(case)
    #ltd.plot.BAplots02(mir, False, printFigs=True,)

#================================================================================================
""" Long-term thesis simulations """
printFigs = True
mirList = []
mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTfdF.mir') # forcast demand ideal
mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTfdDBnzF.mir') # forcast demand with nz
mirList.append( mirLoc )
#mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTwrF.mir') # wind ramp
#mirList.append( mirLoc )
mirLoc = os.path.join(dirname, 'delme','200326-smLT','smLTwrDBnzF.mir') # wind ramp
mirList.append( mirLoc )

# BAAL testing
#for case in mirList:
    #mir = ltd.data.readMirror(case)
    #ltd.plot.BAALtest(mir, False, True)

#ltd.plot.AreaPLoad(mir, False, printFigs)
#ltd.plot.AreaPe(mir, False, printFigs)
#ltd.plot.AreaPm(mir, False, printFigs)

for mirLoc in mirList:
    mir = ltd.data.readMirror(mirLoc)
    #ltd.plot.BAplots02(mir, False, printFigs)
    ltd.plot.branchMVAR(mir, 8, [9], False, printFigs) # per area, legend inside right
    
    #ltd.plot.BAplots02detail(mir, [100,120], False, printFigs)
    #ltd.plot.sysShuntV(mir, False, printFigs)
    #ltd.plot.sysShuntMVAR(mir,  False, printFigs)
    #ltd.plot.sysPe(mir, False, printFigs)
    #ltd.plot.areaPL(mir, False, printFigs)

#ltd.plot.PloadIEEE2(mir,False, printFigs=True, miniFlag = False)

#ltd.plot.sysPePmFLoad2(mir, False, printFigs)
