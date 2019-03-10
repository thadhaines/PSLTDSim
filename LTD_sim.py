"""
Developement file that acts as main
VS may require default ironpython environment (no bit declaration)
"""

import os
import subprocess
import signal
import time
import __builtin__

# import custom package and make truly global
import psltdsim as ltd
__builtin__.ltd = ltd

ltd.terminal.dispCodeTitle()

print(os.getcwd())

# workaround for interactive mode runs (Use as required)
#os.chdir(r"...")
#print(os.getcwd())

simNotes = """
Retest of ipy code after refactor - simple step up and down with gov
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.5,
    'endTime': 60.0,
    'slackTol': .25,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; TODO: Incoroporate into simulation (probably)

    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'Euler',

    # Data Export Parameters
    'fileDirectory' : "\\verification\\refactor\\", # relative path must exist before simulation
    'fileName' : 'pgovAgain01',
    'exportDict' : 1, # when using python 3 no need to export dicts.
    'exportMat': 1, # requies exportDict == 1 to work
    }

# Fast debug case switching
# TODO: enable new dyd replacement...
# TODO: incorporate ltdPath into simulation
test_case = 0
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc.dyd",
               #r"C:\LTD\pslf_systems\eele554\ee554.ltd.dyd", #pgov1 on gen 2
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
elif test_case == 4:
    savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"
    dydPath = [r"C:\LTD\pslf_systems\GE_ex\g4_a.dyd",
               r"C:\LTD\pslf_systems\GE_ex\g4_a.ltd", #pgov1 on slacks
               ]

# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : savPath,
    'dydPath': dydPath,
    }
del savPath, dydPath

### Start Simulation functions calls
ltd.init_PSLF(locations)

# mirror arguments: locations, simParams, debug flag
initStart = time.time()
mir = ltd.mirror.Mirror(locations, simParams, 0)
mir.notes = simNotes # update notes before export

# TODO: enable entering of perturbance via some parsed text file - keep in IPY
# Pertrubances configured for test case (eele)
# step up and down (pgov test)
ltd.mirror.addPerturbance(mir,'Load',[3],'Step',['P',2,101]) # quick 1 MW step
ltd.mirror.addPerturbance(mir,'Load',[3],'Step',['P',30,100]) # quick 1 MW step
print('Init time: %f' % (time.time() - initStart))

ltd.data.saveMirror(mir, simParams)

simStart = time.time()
mir.runSim()
simEnd = time.time()

ltd.terminal.dispSimResults(mir) # for terminal output

print('Simulation time: %f' % (simEnd - simStart))

"""
# Data export - no need to test in ipy
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

## update to make mat using python 3.6
if simParams['fileDirectory']:
        cwd = os.getcwd()
        os.chdir(cwd + simParams['fileDirectory'])

sysDict = makeModelDictionary(mir)
mirD ={'varName01':sysDict}
import scipy.io as sio
sio.savemat('varName01', mirD)
print("saved")
"""
# raw_input("Press <Enter> to Continue. . . . ") # Not always needed to hold open console
