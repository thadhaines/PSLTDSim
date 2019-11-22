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
os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")

print(os.getcwd())

debug = 1

simNotes = """
DEBUG
"""

testCase = r".\testCases\BA_tests\miniWECC3A2IACE.py"
testCase = r".\testCases\191122-fullWECC\fWECCstep1.py"
#testCase = r".\testCases\sixMachine\sixMachineStep2.py"
exec(open(testCase).read());
ltd.terminal.dispCodeTitle()


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

import time # required for timings...
__builtin__.time = time

# Create system mirror
#mir = ltd.mirror.Mirror(locations, simParams, simNotes, debug, AMQPdebug, debugTimer)

zBus = col.BusDAO.FindByType(0)
if len(zBus) == 1:
    # If only 1 slack, obvious choice
    gSlackB = zBus[0]
else:
    for bus in zBus:
        print(bus.Islnum)
        if bus.Islnum == 1:
            # otherwise, find slack in island 1
            gSlackB = bus

print('debug Stop')