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

print('debug Stop')