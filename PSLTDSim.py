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

# List of simulation parameter .py files:
batchList =[

    # initial tgov1 testing
    #r".\testCases\ee554\ee554noGovStepUp.py",
    #r".\testCases\ee554\ee554noGovStepDown.py",
    #r".\testCases\ee554\ee554noGovStepss.py",
    #r".\testCases\ee554\ee5541GovSteps.py", #*
    #r".\testCases\ee554\ee5542GovSteps.py",

    # Perturbance from ltd file testing
    #r".\testCases\ee554\ee5541GovRampARel.py",
    #r".\testCases\ee554\ee5541GovRampAPer.py",
    #r".\testCases\ee554\ee5541GovRampAAbs.py",
    #r".\testCases\ee554\ee5541GovRampsPer.py",
    #r".\testCases\ee554\ee5541GovRampsAbs.py",
    #r".\testCases\ee554\ee5541GovRampsGens.py",
    #r".\testCases\ee554\ee554PrefStep.py", #*
    #r".\testCases\ee554\see554PmStepRamp.py", #*

    # AMQP Message grouping speedup Tests
    #r".\testCases\miniWECCstepGroupA.py",
    #r".\testCases\miniWECCstepGroupB.py",
    #r".\testCases\miniWECCstepGroupC.py",

    #r".\testCases\kundur\kundurLoadRamp0.py",# 2 area, 1 slack ramp down
    #r".\testCases\kundur\kundurLoadRamp1.py",
    #r".\testCases\kundur\kundurLoadRamp2.py",
    #r".\testCases\kundur\kundurLoadRamp3.py",

    #r".\testCases\kundur\kundurLoadStep0.py",# 2 area, 1 slack 
    #r".\testCases\kundur\kundurLoadStep1.py",
    #r".\testCases\kundur\kundurLoadStep2.py",
    #r".\testCases\kundur\kundurLoadStep3.py",

    #r".\testCases\kundurLoadStepShunt0.py", #*
    #r".\testCases\kundurLoadRampBranch0.py", #*

    # simple gen trips
    #r".\testCases\kundur\kundurGenTrip00.py",
    #r".\testCases\kundur\kundurGenTrip01.py",
    #r".\testCases\kundur\kundurGenTrip02.py",
    #r".\testCases\kundur\kundurGenTrip03.py",

    # more complex gen trip off/on and ramp pm
    #r".\testCases\kundur\kundurGenTrip22.py", #*
    
    # All six machine simulations seem to work correctly
    # Six Machine
    #r".\testCases\sixMachine\sixMachineStep2.py",
    #r".\testCases\sixMachine\sixMachineStep3.py",
    #r".\testCases\sixMachine\sixMachineStep4.py",
    #r".\testCases\sixMachine\sixMachineStep5.py", # step Pm of gov gen

    #r".\testCases\sixMachine\sixMachineRamp2.py",
    #r".\testCases\sixMachine\sixMachineRamp3.py",

    # Six Machine Trips
    #r".\testCases\sixMachine\sixMachineTrip01.py", # Gen trip off/on
    #r".\testCases\sixMachine\sixMachineBTrip0.py", # Branch Tripping off
    #r".\testCases\sixMachine\sixMachineTrip2.py", # Branch Tripping off/on
    #r".\testCases\sixMachine\sixMachineTrip1.py", # Gen 'trip' on - can't get PSLF to do the thing...
    
    # six machine BA testing
    #r".\testCases\sixMachine\sixMachineStepBA.py",
    #r".\testCases\sixMachine\sixMachineStepBA0.py",
    #r".\testCases\sixMachine\sixMachineStepBA1.py",
    #r".\testCases\sixMachine\sixMachineStepBA2.py",
    #r".\testCases\sixMachine\sixMachineStepBA3.py",
    #r".\testCases\sixMachine\sixMachineStepBA4.py",
    
    # mini wecc tests - Confirmed working 7/9/19
    #r".\testCases\miniWECC\miniWECCstep0.py",
    #r".\testCases\miniWECC\miniWECCstep1.py",
    #r".\testCases\miniWECC\miniWECCstep2.py",
    #r".\testCases\miniWECC\miniWECCstep3.py",

    #r".\testCases\miniWECC\miniWECCcrash.py",

    #r".\testCases\miniWECC\miniWECCgenTrip0.py",

    # Multi Area miniWECC
    #r".\testCases\miniWECC3Area\miniWECC3A00.py", # simple step (unscaled system)
    #r".\testCases\miniWECC3Area\miniWECC3A0.py", # simple step
    #r".\testCases\miniWECC3Area\miniWECC3A1.py", # BA response, TLB type 2
    #r".\testCases\miniWECC3Area\miniWECC3A2.py", # BA response, TLB type 0

    # Final Validations
    #r".\testCases\sixMachine\sixMachineStep1.py",
    #r".\testCases\sixMachine\sixMachineRamp1.py",
    #r".\testCases\sixMachine\sixMachineTrip0.py", # Gen trip off

    #r".\testCases\miniWECCLTD\miniWECC3Astep.py",
    #r".\testCases\miniWECCLTD\miniWECC3Aramp.py",
    #r".\testCases\miniWECCLTD\miniWECCgenTrip0.py",

    # Same as above miniWECC tests, but with PSS
    #r".\testCases\miniWECCLTDPSS\miniWECC3Astep.py",
    #r".\testCases\miniWECCLTDPSS\miniWECC3Aramp.py",
    #r".\testCases\miniWECCLTDPSS\miniWECCgenTrip0.py",

    # BA research with AGC
    #r".\testCases\BA_tests\miniWECC3A0.py", # BA response, TLB type 0, -1000 MW gen in area 3
    #r".\testCases\BA_tests\miniWECC3A1IACE.py", # BA response, TLB type 2, -1000 MW gen in area 3 with IACE
    #r".\testCases\BA_tests\miniWECC3A1.py", # BA response, TLB type 2, -1000 MW gen in area 3

    #r".\testCases\BA_tests\miniWECC3A2.py", # BA response, TLB type 2, + 400MW wind in area 1
    #r".\testCases\BA_tests\miniWECC3A2IACE.py", # BA response, TLB type 2, + 400MW wind in area 1 with IACE
    #r".\testCases\BA_tests\miniWECC3A3.py", # BA response, TLB type 2, + 400MW wind in area 2
    #r".\testCases\BA_tests\miniWECC3A4.py", # BA response, TLB type 0, + 400MW wind in area 1
    #r".\testCases\BA_tests\miniWECC3A5.py", # BA response, TLB type 0, + 400MW wind in area 2

    # IEEE paper experiments
    r".\testCases\IEEEpaper\miniWECCgenTrip.py", # 1500MW trip in area 3, no gov response in area 3 - AGC


            ]

# Batch Run Parameters
dispResults = False
dispTiming = True
makePlot = True

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
    #debugTimer = 1

    print('*** Case {}/{}'.format(case, len(batchList)))
    print('*** %s' % testCase)
    print('\n*** Checking simulation files...')
    userFiles = [savPath] + dydPath + [ltdPath]
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
               'debugTimer' : debugTimer,
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
            
            ltd.plot.BAplots01(mir, False)
            ltd.plot.sysPePmFLoad(mir, True)
            waitTime += time.time() - wait_start
        else:
            
            ltd.plot.BAplots01(mir, False,)
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