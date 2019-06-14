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
elif test_case == 5: # testing of ggov casting
    savPath = r"C:\LTD\pslf_systems\eele554\ggov1\ee554.sav"
    dydPath = [r"C:\LTD\pslf_systems\eele554\ggov1\ee554.ggov1.dyd"]
    ltdPath = [r"C:\LTD\pslf_systems\eele554\ggov1\ee554.BigUpStep.ltd"]
"""

# List of simulation parameter .py files:
batchList =[
    # mini wecc tests
    #r".\testCases\miniWECCstep0.py",
    #r".\testCases\miniWECCstep1.py",
    #r".\testCases\miniWECCstep2.py",
    #r".\testCases\miniWECCstep3.py",

    #r".\testCases\miniWECCcrash.py",

    #r".\testCases\microWECCstep.py",

    # initial tgov1 testing
    #r".\testCases\ee554noGovStepUp.py",
    #r".\testCases\ee554noGovStepDown.py",
    #r".\testCases\ee554noGovSteps.py",
    #r".\testCases\ee5541GovSteps.py", #*
    #r".\testCases\ee5542GovSteps.py",

    # Perturbance from ltd file testing
    #r".\testCases\ee5541GovRampARel.py",
    #r".\testCases\ee5541GovRampAPer.py",
    #r".\testCases\ee5541GovRampAAbs.py",
    #r".\testCases\ee5541GovRampsPer.py",
    #r".\testCases\ee5541GovRampsAbs.py",
    #r".\testCases\ee5541GovRampsGens.py",
    #r".\testCases\ee554PrefStep.py", #*
    #r".\testCases\ee554PmStepRamp.py", #*

    # AMQP Message grouping speedup Tests
    #r".\testCases\miniWECCstepGroupA.py",
    #r".\testCases\miniWECCstepGroupB.py",
    #r".\testCases\miniWECCstepGroupC.py",

    #r".\testCases\kundurLoadRamp0.py",# 2 area, 1 slack ramp down
    #r".\testCases\kundurLoadRamp1.py",
    #r".\testCases\kundurLoadRamp2.py",
    #r".\testCases\kundurLoadRamp3.py",

    #r".\testCases\kundurLoadRamp10.py",# 2 area, 1 slack 40 sec ramp
    #r".\testCases\kundurLoadRamp11.py",
    #r".\testCases\kundurLoadRamp12.py",
    #r".\testCases\kundurLoadRamp13.py",

    #r".\testCases\kundurLoadStep0.py",# 2 area, 1 slack 
    #r".\testCases\kundurLoadStep1.py",
    #r".\testCases\kundurLoadStep2.py",
    #r".\testCases\kundurLoadStep3.py",

    #r".\testCases\kundurLoadStepShunt0.py", #*
    #r".\testCases\kundurLoadRampBranch0.py", #*

    # simple gen trips
    #r".\testCases\kundurGenTrip00.py",
    #r".\testCases\kundurGenTrip01.py",
    #r".\testCases\kundurGenTrip02.py",
    #r".\testCases\kundurGenTrip03.py",

    # more complex gen trip off/on and ramp pm
    #r".\testCases\kundurGenTrip22.py", #*

    # tests of damping and Reff
    #r".\testCases\kundurReff0.py", # 3/4 same gens
    #r".\testCases\kundurReff2.py", # 2 govs the same, 1 un gov
    #r".\testCases\kundurReff3.py", # dif H, mwcap
    r".\testCases\kundurReff4.py", # dif mbase

    #r".\testCases\kundurReff0damping.py",
            ]

# Batch Run Parameters
dispResults = False
dispTiming = False
makePlot = False

# Batch run counters
case = 0
failed = 0
failedTestCase = []
crashedTestCase = []
batchStart = time.time()
waitTime = 0.0

for testCase in batchList:
    fail = False
    case+=1

    exec(open(testCase).read());
    ltd.terminal.dispCodeTitle()

    # override debugs
    #debug = 1
    #AMQPdebug = 1

    print('*** Case {}/{}'.format(case, len(batchList)))
    print('*** %s' % testCase)
    print('\n*** Checking simulation files...')
    userFiles = [savPath] + dydPath + ltdPath
    for fileLoc in (userFiles):
        if not os.path.isfile(fileLoc):
            print('*** Test Case Fail: %s' % testCase)
            print('File does not exist: ' + fileLoc)
            failedTestCase.append( testCase + '\nFile does not exist: ' + fileLoc)
            fail = True
    if fail:
        failed += 1
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
    if dispResults:
        ltd.terminal.dispSimResults(mir)
    if dispTiming:
        ltd.terminal.dispSimTandC(mir)    
    if makePlot:
        # only hold for last plot
        if case == len(batchList):
            wait_start = time.time()
            print('\n*** Waiting for plot to close...')
            ltd.plot.sysPQVF(mir, False)
            ltd.plot.sysPePmFLoad(mir, True)
            waitTime += time.time() - wait_start
        else:
            ltd.plot.sysPQVF(mir, False)
            ltd.plot.sysPePmFLoad(mir ,False)

# End of Batch Output
batchTime = time.time() - batchStart - waitTime
print('\n*** Successfully ran %d/%d Test Cases in %.2f seconds.' % (case-failed, 
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