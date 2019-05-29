"""Python 3 main file"""
import os
import subprocess
import signal
import pika
import builtins
import time
import numpy as np
import scipy.signal as sig
from scipy.integrate import solve_ivp

import psltdsim as ltd

# for truly global imported packages
builtins.np = np
builtins.sig = sig
builtins.solve_ivp = solve_ivp
builtins.time = time
builtins.ltd = ltd

print('Current Working Directory: %s' % os.getcwd())

# workaround for interactive mode runs (Use as required)
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")
#print(os.getcwd())
"""
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = [r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"]

elif test_case == 4:
    savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"
    dydPath = [r"C:\LTD\pslf_systems\GE_ex\g4_a.dyd",
               r"C:\LTD\pslf_systems\GE_ex\g4_a.ltd", #pgov1 on slacks
               ]
elif test_case == 5: # testing of ggov casting
    savPath = r"C:\LTD\pslf_systems\eele554\ggov1\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ggov1\ee554.ggov1.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ggov1\ee554.BigUpStep.ltd"]
"""

# List of simulation parameter .py files:
batchList =[
    r".\testCases\miniWECCstepTS02.py",
    r".\testCases\miniWECCstepTS05.py",
    r".\testCases\miniWECCstepTS10.py",
    r".\testCases\miniWECCstepTS10.py",
    r".\testCases\miniWECCstepTS20.py",
    r".\testCases\ee554noGovStepUp.py",
    r".\testCases\ee554noGovStepDown.py",
    r".\testCases\ee554noGovSteps.py",
    r".\testCases\ee5541GovSteps.py",
    r".\testCases\ee5542GovSteps.py",
    r".\testCases\ee5541GovRamp.py",
    r".\testCases\microWECCstep.py",
            ]

# Batch Run Variable Initialization
case = 0
failed = 0
failedTestCase =[]
crashedTestCase = []
batchStart = time.time()

for testCase in batchList:
    fail = False
    case+=1

    exec(open(testCase).read());
    ltd.terminal.dispCodeTitle()

    # override debugs
    #debug = 1
    #AMQPdebug = 1

    print('*** Case %d/%d' % (case, len(batchList)))

    print('*** Checking simulation files...')
    userFiles = [savPath] + dydPath + ltdPath
    for fileLoc in (userFiles):
        if not os.path.isfile(fileLoc):
            print('*** Test Case Fail: %s' % testCase)
            print('File does not exist: ' + fileLoc)
            failedTestCase.append( testCase + '\nFile does not exist: ' + fileLoc)
            fail = True
            failed += 1

    if fail:
        continue
    
    # Required Paths Dictionary
    locations = {
        # path to folder containing middleware dll (default behavior)
        'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
        # path to folder containing PSLF license (default behavior)
        'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
        'savPath' : savPath,
        'dydPath': dydPath,
        'ltdPath' : ltdPath,
        }

    # Init PY3 AMQP
    print('*** Initializing AMQP...')
    init_start = time.time()
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
    print('*** Creating IPY process...')
    cmd = "ipy32 IPY_PSLTDSim.py"
    ipyProc = subprocess.Popen(cmd)

    # Wait for mirror message
    print('*** Waiting for mirror...')
    PY3.receive('toPY3',PY3.redirect)
    print(mir)
    PY3.mirror = mir

    # begin PY3 simulation loop 
    ltd.runSimPY3(mir, PY3)
    # ensure IPY closes
    ipyProc.kill()

    if mir.sysCrash:
        crashedTestCase.append(testCase)

    # Additional optional post simulation outputs
    #ltd.terminal.dispSimResults(mir)
    ltd.terminal.dispSimTandC(mir)
    #ltd.plot.allPmDynamics(mir)
    #ltd.plot.sysPePmFLoad(mir)

# End of Batch Output
batchTime = time.time() - batchStart
print('\n*** Successfully Ran %d/%d Test Cases in %.2f seconds.' % (case-failed, 
                                                     len(batchList),
                                                     batchTime))

if len(crashedTestCase) > 0:
    print('\n*** Crashed Test Cases:')
    for case in crashedTestCase:
        print(case)

if len(failedTestCase) > 0:
    print('\n*** Failed Test Cases:')
    for case in failedTestCase:
        print(case)