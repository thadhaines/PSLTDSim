"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

import os
import __builtin__

from parseDyd import *
from distPe import *
from combinedSwing import *
from saveMirror import saveMirror
from findFunctions import *
from PerturbanceAgents import *

# workaround for interactive mode runs (Use only if required)
print(os.getcwd())
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
#print(os.getcwd())

# Simulation Parameters
timeStep = 1.0
endTime = 20.0
slackTol = 5.0
Hsys = 0.0 # MW*sec of entire system, if !> 0.0, will be calculated in code
Dsys = 0.0 # PU; TODO: Incoroporate into simulation (probably)

# Required Paths
## full path to middleware dll
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  
## path to folder containing PSLF license
pslfPath = r"C:\Program Files (x86)\GE PSLF"  

# fast debug case switching
test_case = 2
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = r"C:\LTD\pslf_systems\eele554\ee554.dyd"
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )
del fullMiddlewareFilePath, pslfPath, savPath, dydPath

simParams = (
    timeStep,
    endTime,
    slackTol,
    Hsys,
    Dsys,
    )
del timeStep, endTime, slackTol, Hsys, Dsys

# these files will change after refactor
execfile('initPSLF.py')

# imports must occur after intiPSLF.py
from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
from Model import Model

execfile('makeGlobals.py')

# mirror arguments: locations, simParams, debug flag
mir = Model(locations, simParams, 0)

# Pertrubances configured for test case (mini wecc)
# mini wecc slackTolerance should be conidered
mir.addPert('Load',[8],'Step',['P',2,4385]) # step down 
mir.addPert('Load',[8],'Step',['P',12,4420]) # step up
mir.addPert('Load',[8],'Step',['P',17,400]) # step to norm

mir.runSim()

print("Log and Step check of Load, Pacc, and sys f:")
print("Time\tSt\tPacc\tsys f\tdelta f\t\tSlackPe\tGen2Pe")
for x in range(mir.c_dp):
    print("%d\t%d\t%.2f\t%.5f\t%.6f\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Load[0].r_St[x],
        mir.r_ss_Pacc[x],
        mir.r_f[x],
        mir.r_deltaF[x],
        mir.Machines[0].r_Pe[x],
        mir.Machines[1].r_Pe[x],))

# Testing of data export
from saveMirror import saveMirror
# Saving doesn't work in interactive mode.... truncates pickle data
saveMirror(mir,'exportTestMiniF5Mir')

from makeModelDictionary import makeModelDictionary
from saveModelDictionary import saveModelDictionary

d = makeModelDictionary(mir)
saveModelDictionary(d,'exportTestMiniF5D')

raw_input("Press <Enter> to Continue. . . . ")
