""" IPY only simulation - Used as debug of mirror creation
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
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
#print(os.getcwd())

debug = 1

simNotes = """
Retest of ipy code after refactor - simple step up and down with gov
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.25,
    'endTime': 1.5,
    'slackTol': 1.0,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; TODO: Incoroporate into simulation (probably)

    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'euler',

    # Data Export Parameters
    'fileDirectory' : "\\verification\\miniWeccTest01\\", # relative path must exist before simulation
    'fileName' : 'miniWECC_loadStep06IPY',

    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

# Fast debug case switching
test_case = 3 #'tGovRamp'
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\tgov\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.excNoGov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.ramp.ltd"]
   
elif test_case == 'tGovRamp':
    savPath = r"C:\LTD\pslf_systems\eele554\tgov\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.exc1Gov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.ramp.ltd"]
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = [r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"]
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"]
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav"
    dydPath = [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1.dyd"]
elif test_case == 4:
    savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"
    dydPath = [r"C:\LTD\pslf_systems\GE_ex\g4_a.dyd",
               r"C:\LTD\pslf_systems\GE_ex\g4_a.ltd", #pgov1 on slacks
               ]

if not 'ltdPath' in dir(): # handle undefined ltdPath
    ltdPath = None

# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : savPath,
    'dydPath': dydPath,
    'ltdPath': ltdPath,
    }
del savPath, dydPath

### Start Simulation functions calls
ltd.init_PSLF(locations)

"""
# mirror arguments: locations, simParams, debug flag
initStart = time.time()
mir = ltd.mirror.Mirror(locations, simParams, simNotes, debug)
print('Init time: %f' % (time.time() - initStart))

#ltd.data.saveMirror(mir, simParams) # test mirror export

simStart = time.time()
ltd.runSim_OG(mir)
simEnd = time.time()

ltd.terminal.dispSimResults(mir) # for terminal output

print('Simulation time: %f' % (simEnd - simStart))


# Data export
if simParams['exportFinalMirror']:
    simParams['fileName'] += 'F'
    ltd.data.saveMirror(mir, simParams)

if simParams['exportDict']:

    dictPath = ltd.data.exportDict(mir)

    d = ltd.data.loadMirrorDictionary(dictPath)
    #print('debug for dictionary saving loading')

"""

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
"""
"""


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
