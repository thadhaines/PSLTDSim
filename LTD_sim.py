"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

import os
import subprocess
import signal
import __builtin__

# workaround for interactive mode runs (Use only if required)
print(os.getcwd())
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
#os.chdir(r"D:\Users\jhaines\Source\Repos\thadhaines\LTD_sim")
#print(os.getcwd())

from parseDyd import *
from distPe import *
from combinedSwing import *
from findFunctions import *
from PerturbanceAgents import *
from pgov1Agent import *
from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
from Model import Model
from makeModelDictionary import makeModelDictionary
from saveModelDictionary import saveModelDictionary

execfile('mergeDicts.py')

simNotes = """
-20 MW load step at t=2
sim time = 20 seconds, 
changed slackTol to 0.25. Timestep = 1
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 20.0,
    'slackTol': 30,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; TODO: Incoroporate into simulation (probably)

    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'Euler',

    # Data Export Parameters
    'fileDirectory' : r"\\verification\\noGovLoadStep\\loadStepDown\\", # relative path must exist before simulation
    'fileName' : 'quickie',
    'exportDict' : 1,
    'exportMat': 1, # requies exportDict == 1 to work
    }

# fast debug case switching
# TODO: enable new dyd replacement
test_case = 0
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc.dyd",
               #r"C:\LTD\pslf_systems\eele554\ee554.ltd.dyd",
               ]
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = [r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"]
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"]
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = [r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"]

# Required Paths
locations = {
    # full path to middleware dll
    'fullMiddlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : savPath,
    'dydPath': dydPath,
    }
del savPath, dydPath

# these files will change after refactor, required after locations definition
execfile('initPSLF.py')
execfile('makeGlobals.py')

# mirror arguments: locations, simParams, debug flag
mir = Model(locations, simParams, 1)

# Pertrubances configured for test case (eele)
# step up and down (pgov test)
#mir.addPert('Load',[3],'Step',['P',2,101]) # quick 1 MW step
#mir.addPert('Load',[3],'Step',['P',30,100]) # quick 1 MW step

# single steps up or down
mir.addPert('Load',[3],'Step',['P',2,80]) # step load down to 80 MW 
#mir.addPert('Load',[3,'2'],'Step',['St',2,1]) # step 20 MW load bus on 

mir.runSim()

mir.notes = simNotes

# Terminal display output for immediate results
print("Log and Step check of Load, Pacc, and sys f:")
print("Time\tSt\tPacc\tsys f\tdelta f\t\tSlackPe\tGen2Pe")
for x in range(mir.c_dp-1):
    print("%d\t%d\t%.2f\t%.5f\t%.6f\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Load[0].r_St[x],
        mir.r_ss_Pacc[x],
        mir.r_f[x],
        mir.r_deltaF[x],
        mir.Slack[0].r_Pe[x],
        mir.Machines[1].r_Pe[x],))
print('End of simulation data.')

# Data export
if simParams['exportDict']:
    # Change current working directory to data destination.
    cwd = os.getcwd()
    if simParams['fileDirectory'] :
        os.chdir(cwd + simParams['fileDirectory'])

    dictName = simParams['fileName']
    D = makeModelDictionary(mir)
    savedName = saveModelDictionary(D,dictName)
    os.chdir(cwd)

    if  simParams['exportMat']:
        # use cmd to run python 3 32 bit script...
        cmd = "py -3-32 makeMat.py " + savedName +" " + dictName  + " "+ simParams['fileDirectory'] 

        matProc = subprocess.Popen(cmd)
        matReturnCode = matProc.wait()
        matProc.send_signal(signal.SIGTERM)

# attempts to delete .pkl file fails -> in use by another process, reslove?
#del matProc
#os.remove(savedName)
#print('%s Deleted.' % savedName)

# raw_input("Press <Enter> to Continue. . . . ") # Not always needed to hold open console