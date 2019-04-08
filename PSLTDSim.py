"""Python 3 main file"""
import os
import subprocess
import signal
import time
import builtins
import pika

# for truly global numpy scipy things
import numpy as np
import scipy.signal as sig
from scipy.integrate import solve_ivp

builtins.np = np
builtins.sig = sig
builtins.solve_ivp = solve_ivp

# import custom package and make truly global
import psltdsim as ltd
builtins.ltd = ltd

ltd.terminal.dispCodeTitle()
print(os.getcwd())

# workaround for interactive mode runs (Use as required)
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")
#print(os.getcwd())

# for extended terminal output
debug = 1
AMQPdebug = 0

simNotes = """
Step of Tgov system...
using 'accepted' model
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
    'integrationMethod' : 'rk45',

    # Data Export Parameters
    'fileDirectory' : "\\verification\\refactor\\tgov_steps\\", # relative path must exist before simulation
    'fileName' : 'tGovStep04',
    'exportFinalMirror': 1, #
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'exportMat': 1, # requies exportDict == 1 to work
    }

# Fast debug case switching
# TODO: MAYBE enable new dyd replacement... (too cute?)
test_case = 'tGovSteps'
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.BigUpStep.ltd"]
elif test_case == 'bigUp':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.BigUpStep.ltd"]
elif test_case == 'bigDown':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.BigDownStep.ltd"]
elif test_case == 'noGovSteps':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.steps.ltd"]
elif test_case == 'tGovSteps':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc1Gov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.steps.ltd"]
elif test_case == 'tGov2Steps':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc2Gov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.steps.ltd"]
elif test_case == 'tGovRamp':
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc1Gov.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.ramp.ltd"]

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
    'ltdPath' : ltdPath,
    }
del savPath, dydPath, ltdPath, test_case

init_start = time.time()
# Init PY3 AMQP
host = '127.0.0.1'
PY3 = ltd.amqp.AMQPAgent('PY3',host)

# Clear AMQP queues
ltd.amqp.clearQ(host, ['toPY3', 'toIPY'])

# create and send init msg
initMsg = {'msgType': 'init',
           'locations': locations,
           'simParams': simParams,
           'simNotes': simNotes,
           'debug': debug,
           'AMQPdebug' : AMQPdebug,
           }
PY3.send('toIPY', initMsg)

# Start IPY - assumes ironpython on path
cmd = "ipy32 IPY_PSLTDSim.py"
ipyProc = subprocess.Popen(cmd)

# Wait for mirror message
PY3.receive('toPY3',PY3.redirect)
print('py3 main...')
print(mir)
PY3.mirror = mir
## begin PY3 simulation loop 
sim_start = time.time()
ltd.runSimPY3(mir, PY3)
sim_end = time.time()

# Post simulation operations
ltd.terminal.dispSimResults(mir)

if simParams['exportFinalMirror']:
    simParams['fileName'] += 'F'
    ltd.data.saveMirror(mir, simParams)

if simParams['exportMat']:
    ltd.data.exportMat(mir, simParams)

print("init time:\t %f" % (sim_start-init_start) )
print("sim time:\t %f" % (sim_end-sim_start) )

ltd.plot.sysPePmFLoad(mir)

print('end of debug test run')