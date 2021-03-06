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
    #r".\testCases\IEEEpaper\miniWECCgenTrip.py", # 1500MW trip in area 3, no gov response in area 3 - AGC
    #r".\testCases\IEEEpaper\genTripHighRnoDB.py", # 1500MW trip in area 3
    #r".\testCases\IEEEpaper\genTripEqualRnoDB.py", # 1500MW trip in area 3
    #r".\testCases\IEEEpaper\genTripEqualRstepDB.py", # 1500MW trip in area 3
    #r".\testCases\IEEEpaper\genTripEqualRnonLinDB.py", # 1500MW trip in area 3


    #r".\testCases\IEEEpaper\windramp.py", # 400MW trip in area 3 nldroop
    #r".\testCases\IEEEpaper\windramp2.py", # -1500 MW ramp in area 3 nldroop
    #r".\testCases\IEEEpaper\windrampNoDB.py", # 400MW trip in area 3
    #r".\testCases\IEEEpaper\windrampNoDBFast.py", # 400MW trip in area 3, 3 second AGC dispatch
    #r".\testCases\IEEEpaper\windrampNoDBSlow.py", # 400MW trip in area 3, 15 second AGC dispatch
    #r".\testCases\IEEEpaper\windrampNoDBSlowGain.py", # 400MW trip in area 3, 15 second AGC dispatch, ACE*3
    #r".\testCases\IEEEpaper\windrampNoDBFastGain.py", # 400MW trip in area 3, 3 second AGC dispatch, ACE*3
    #r".\testCases\IEEEpaper\windrampNoDBFastGainIACE.py", # 400MW trip in area 3, 3 second AGC dispatch, ACE*3, include IACE
    #r".\testCases\IEEEpaper\windrampNoDBFastGainIACENoFilter.py", # 400MW trip in area 3, 3 second AGC dispatch, ACE*3, include IACE
    #r".\testCases\IEEEpaper\windrampNoDBFastGainIACENoB.py", # 400MW trip in area 3, 3 second AGC dispatch, ACE*3, include IACE no B

    # Noise Agent Testing
    #r".\testCases\noiseTest\miniWECCnoise.py", # testing of noise agent
    #r".\testCases\noiseTest\sixMachineNoise.py", # testing of noise agent
    #r".\testCases\noiseTest\sixMachineNoise2.py", # testing of noise agent
    #r".\testCases\noiseTest\sixMachineNoise3.py", # testing of noise agent
    #r".\testCases\noiseTest\sixMachineNoise4.py", # testing of noise agent
    #r".\testCases\noiseTest\sixMachineNoise5.py", # testing of noise agent

    #r".\testCases\noiseTest\sixMachineNoiseX.py", # testing of noise agent

    # MiniWECC noise testing 10/23/19
    #r".\testCases\191023_db\miniWECCBASE.py", # base case
    # 1 second timestep With AGC
    #r".\testCases\191023_db\mw10StepDBAGC.py", # 
    #r".\testCases\191023_db\mw10NoStepDBAGC.py", # 
    #r".\testCases\191023_db\mw10NLdroopDBAGC.py", # 
    #r".\testCases\191023_db\mw10NoDBAGC.py", # 
    # No AGC
    #r".\testCases\191023_db\mw10StepDBNoAGC.py", # 
    #r".\testCases\191023_db\mw10NoStepDBNoAGC.py", # 
    #r".\testCases\191023_db\mw10NLdroopDBNoAGC.py", # 
    #r".\testCases\191023_db\mw10NoDBNoAGC.py", # 

    # 0.5 second timestep With AGC
    #r".\testCases\191023_db\mw05StepDBAGC.py", # 
    #r".\testCases\191023_db\mw05NoStepDBAGC.py", # 
    #r".\testCases\191023_db\mw05NLdroopDBAGC.py", # 
    #r".\testCases\191023_db\mw05NoDBAGC.py", # 
    # No AGC
    #r".\testCases\191023_db\mw05StepDBNoAGC.py", # 
    #r".\testCases\191023_db\mw05NoStepDBNoAGC.py", # 
    #r".\testCases\191023_db\mw05NLdroopDBNoAGC.py", # 
    #r".\testCases\191023_db\mw05NoDBNoAGC.py", # 

    # IEEE paper noise tests
    #r".\testCases\191028-paperSims\miniWECCnoiseNoDB.py", # 
    #r".\testCases\191028-paperSims\miniWECCnoiseStepDB.py", # 
    #r".\testCases\191028-paperSims\miniWECCnoiseNoStepDB.py", # 
    #r".\testCases\191028-paperSims\miniWECCnoiseNLdroopDB.py", # 
    #
    # IEEE paper noise tests no AGC
    #r".\testCases\191029-paperSimsNoAGC\miniWECCuniAcc.py", # Universal acceptance sim
    #r".\testCases\191029-paperSimsNoAGC\miniWECCatlAGC.py", # AGC ramp time test
    #r".\testCases\191029-paperSimsNoAGC\miniWECCnoiseNoDB.py", # 
    #r".\testCases\191029-paperSimsNoAGC\miniWECCnoiseStepDB.py", # 
    #r".\testCases\191029-paperSimsNoAGC\miniWECCnoiseNoStepDB.py", # 
    #r".\testCases\191029-paperSimsNoAGC\miniWECCnoiseNLdroopDB.py", # 

    # Testing of generic H and R locations...
    #r".\testCases\191114-genericsTest\sixMachineStepGenMach1.py",
    #r".\testCases\191114-genericsTest\sixMachineStepGenMach2.py",
    #r".\testCases\191114-genericsTest\sixMachineStepGenGov1.py",
    #r".\testCases\191114-genericsTest\sixMachineStepGenGov2.py",
    #r".\testCases\191114-genericsTest\sixMachineStepGenGov3.py",

    # generic miniWECC testing
    #r".\testCases\191118-miniWECCgeneric\genMWstep.py",
    #r".\testCases\191118-miniWECCgeneric\genMWramp.py",
    #r".\testCases\191118-miniWECCgeneric\genMWgenTrip0.py",

    # full wecc
    #r".\testCases\191122-fullWECC\fWECCstep1.py", # tested as working
    #r".\testCases\191209-mysteryWECC\fWECCstep1.py", # Includes islanded things - seems to work... HVDC mismatches... mtTap.p is run alot - provides classic F responnse...

    # Load Controller Test
    #r".\testCases\191214-loadCTRL\sixMachineLoadCTRL.py",
    #r".\testCases\191214-loadCTRL\sixMachineLoadCTRL2.py",
    #r".\testCases\191214-loadCTRL\sixMachineLoadCTRL3.py",

    # Generation Controller Test
    #r".\testCases\191215-genCTRL\sixMachineGenCTRL.py",
    #r".\testCases\191215-genCTRL\sixMachineGenCTRL2.py",
    #r".\testCases\191215-genCTRL\sixMachineGenCTRL3.py",
    
    # Thesis Validations
    r".\testCases\191217-thesisValidation\sixMach\sixMachineStep1.py",
    #r".\testCases\191217-thesisValidation\sixMach\sixMachineRamp1.py",
    #r".\testCases\191217-thesisValidation\sixMach\sixMachineTrip0.py", # Gen trip off

    #r".\testCases\191217-thesisValidation\miniW\miniWECC3Astep.py",
    #r".\testCases\191217-thesisValidation\miniW\miniWECC3Aramp.py",
    #r".\testCases\191217-thesisValidation\miniW\miniWECCgenTrip0.py",

    #r".\testCases\191217-thesisValidation\miniW\miniWECC3AstepPSS.py",
    #r".\testCases\191217-thesisValidation\miniW\miniWECC3ArampPSS.py",
    #r".\testCases\191217-thesisValidation\miniW\miniWECCgenTrip0PSS.py",
    
    #r".\testCases\191217-thesisValidation\wecc\18HSPweccStep.py", # WORKS
    #r".\testCases\191217-thesisValidation\wecc\18HSPweccRamp.py", # crashes after 12 seconds...
    #r".\testCases\191217-thesisValidation\wecc\18HSPweccTrip.py", # NOT DEVELOPED...

    # Delay Tests
    #r".\testCases\200108-delayTest\sixMachineDelayStep1.py", # pref step - AGC tune
    #r".\testCases\200108-delayTest\sixMachineDelayStep2.py", # load step, w delay
    #r".\testCases\200108-delayTest\sixMachineDelayStep3.py", # both delays

    # Delay Scenario
    #r".\testCases\200109-delayScenario1\sixMachineDelayStep1.py", # AGC tuning no delay
    #r".\testCases\200109-delayScenario1\sixMachineDelayStep2.py", # Step - no AGC
    #r".\testCases\200109-delayScenario1\sixMachineDelayStep3.py", # 40 w delay 10 pref
    #r".\testCases\200109-delayScenario1\sixMachineDelayStep4.py", # 40 w delay 10 pref no AGC
    #r".\testCases\200109-delayScenario1\sixMachineDelayStep5.py", # delay,equal amount of delayed gen

    # Mini WECC delay scenario
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep1.py", # No AGC, No Delay
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep1AGC.py", # AGC, No Delay
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep2.py", # No AGC, Delay OR and WA gens
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep2AGC.py", # AGC, Delay OR and WA gens
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep3.py", # No AGC, No Delay - stepping gen instead of load
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep3AGC.py", # No , No Delay - stepping gen instead of load
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep4.py", # No AGC, Delay OR and WA gens - stepping gen instead of load
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep4AGC.py", # AGC, Delay OR and WA gens - stepping gen instead of load
    #r".\testCases\200123-miniWECCdelay\miniWECCDelayStep5AGC.py", # AGC, Delay gens to make swing - stepping gen instead of load

    # Daily Load and Gen Test
    #r".\testCases\200127-dailyControl\sixMachineDailyCTRL.py", # No AGC, Delay OR and WA gens - stepping gen instead of load

    # Shunt Control Test
    #r".\testCases\200131-ShuntControlDev\sixMachineShuntCTRL.py", # No AGC, Delay OR and WA gens - stepping gen instead of load

    # Sunset Scenario
    #r".\testCases\200201-sunset\sixMachineSunset.py", # Sunset in the West
    # Windramp
    #r".\testCases\200202-windramp\sixMachineWindramp.py", # virtual ramp to show shunt work
    
    # DTC Test
    #r".\testCases\200202-DTC\sixMachineDTC.py", # virtual ramp to show shunt work
    # Inertia Perturb test
    #r".\testCases\200203-pertrubH\sixMachineHpert.py", # virtual ramp to show shunt work

    # DTC windramp Test
    #r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC1.py", # virtual ramp to show shunt work V only
    #r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC2.py", # virtual ramp to show shunt work V and Qbr
    #r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC3.py", # virtual ramp to show shunt work V only, gens not ramped 5 min AGC
    #r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC4.py", # virtual ramp to show shunt work V only, gens not ramped 5 min AGC, +inertia ramp + acegain + noise
    #r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC5.py", # virtual ramp to show shunt work V only, gens not ramped 5 min AGC, +inertia ramp + acegain + noise + deadband

    # Q limit test
    #r".\testCases\200210-QlimTest\sixMachineQlim.py", # Ramp of load to test Q limits

    # DTC using gov (lazy)
    #r".\testCases\200220-govDTC\sixMachGovNoDTC.py", # dtc gov testing- base case
    #r".\testCases\200220-govDTC\sixMachGovDTC.py", # dtc gov testing

    # Soft and Hard Tripping
    #r".\testCases\200225-softTrips\sixMachSoftTrip.py", # dtc gov testing- base case
    #r".\testCases\200225-softTrips\sixMachHardTrip.py", # dtc gov testing- base case

    # AGC Variable Frequency Testing
    #r".\testCases\200301-variFreqB\sixMachVariB0.py", # no variable bias
    #r".\testCases\200301-variFreqB\sixMachVariB1.py", # variable bias on

    # Thesis AGC tuning with noise, deadbands
    #r".\testCases\200325-smFinals\smAGCbase1.py", # Area 1 base case
    #r".\testCases\200325-smFinals\smAGCbase2.py", # Area 2 base case
    #r".\testCases\200325-smFinals\smAGCtune1.py", # Area 1 tuning
    #r".\testCases\200325-smFinals\smAGCtune2.py", # Area 2 tuning
    #r".\testCases\200325-smFinals\smAGCdbnz1.py", # Area 1 tuning with db and noise
    #r".\testCases\200325-smFinals\smAGCdbnz2.py", # Area 2 tuning with db and noise
    #r".\testCases\200325-smFinals\smAGCt0In1.py", # both AGC on, area 1 perturbance TLB 0
    #r".\testCases\200325-smFinals\smAGCt4In1.py", # both AGC on, area 1 perturbance TLB 4
    # un needed?
    #r".\testCases\200325-smFinals\smAGCt0Ex1.py", # both AGC on, area 2 perturbance TLB 0
    #r".\testCases\200325-smFinals\smAGCt4Ex1.py", # both AGC on, area 2 perturbance TLB 4

    # Thesis Long-term Simulations
    #r".\testCases\200326-smLT\smLTfd.py", # long-term forcast demand sim
    #r".\testCases\200326-smLT\smLTfdDBnz.py", # long-term forcast demand sim with deadbands and noise
    #r".\testCases\200326-smLT\smLTwr.py", # long-term windramp
    #r".\testCases\200326-smLT\smLTwrDBnz.py", # long-term windramp deadband noise

    # damping and H scaling effect Tests
    #r".\testCases\200329-DandH\smDstep.py", # Damping effect
    #r".\testCases\200329-DandH\smHstep.py", # scaled inertia effect

            ]

# Batch Run Parameters
dispResults = False
dispTiming = False
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

    # read .py file
    exec(open(testCase).read());
    ltd.terminal.dispCodeTitle()

    # override debugs
    #debug = 1
    #AMQPdebug = 1
    #debugTimer = 1

    # ensure file linking can find files
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
            
            #ltd.plot.BAplots01(mir, False)
            #ltd.plot.ValveTravel01(mir, False)

            ltd.plot.sysPePmFLoad2(mir, True)
            waitTime += time.time() - wait_start
        else:
            
            #ltd.plot.BAplots01(mir, False,)
            #ltd.plot.ValveTravel01(mir, False)

            ltd.plot.sysPePmFLoad2(mir ,False)

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