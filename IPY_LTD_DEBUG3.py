""" IPY only simulation - Used to test viability of solving full WECC via ipy
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
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
#os.chdir(r"C:\Users\thad\source\repos\thadhaines\PSLTDSim")
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")

print(os.getcwd())

ltd.terminal.dispCodeTitle()


# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav",
    'dydPath':  [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1Fixed.dyd"], # note that this is a list
    'ltdPath': None,
    }

### Start Simulation functions calls
ltd.init_PSLF(locations)

import time
__builtin__.time = time

# PSLF initialized with WECC case

# Solve case - Maybe rethink these settings for WECC
errorCode = PSLF.SolveCase(
        25, # maxIterations, Solpar.Itnrmx
        0, 	# iterationsBeforeVarLimits, Solpar.Itnrvl
        0,	# flatStart, 
        1,	# tapAdjustment, Solpar.Tapadj
        1,	# switchedShuntAdjustment, Solpar.Swsadj
        1,	# phaseShifterAdjustment, Solpar.Psadj
        0,	# gcdAdjustment, probably Solpar.GcdFlag
        0,	# areaInterchangeAdjustment, 
        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
        0,  # reorder (in dypar default = 0)
        )
print("*** Solution Result: %d" % errorCode)

## Change load on bus 24160 to 580 MW
# get load on external bus num 24160
load = col.LoadDAO.FindByBus(col.BusDAO.FindFirstBusByNumber(24160))
print("*** Current P = %.2f" % load[0].P)

# change P
load[0].P = 580.00
load[0].Save()
del load
## Change load on bus 24133 to 515 MW
# get load on external bus num 24133
load = col.LoadDAO.FindByBus(col.BusDAO.FindFirstBusByNumber(24133))
print("*** Current P = %.2f" % load[0].P)

# change P
load[0].P = 515.00
load[0].Save()
del load

# Ensure load actually changed in PSLF
load = col.LoadDAO.FindByBus(col.BusDAO.FindFirstBusByNumber(24160))
print("*** Updated P = %.2f" % load[0].P)
# Ensure load actually changed in PSLF
load = col.LoadDAO.FindByBus(col.BusDAO.FindFirstBusByNumber(24133))
print("*** Updated P = %.2f" % load[0].P)

# solve case again
errorCode = PSLF.SolveCase(
        25, # maxIterations, Solpar.Itnrmx
        0, 	# iterationsBeforeVarLimits, Solpar.Itnrvl
        0,	# flatStart, 
        1,	# tapAdjustment, Solpar.Tapadj
        1,	# switchedShuntAdjustment, Solpar.Swsadj
        1,	# phaseShifterAdjustment, Solpar.Psadj
        0,	# gcdAdjustment, probably Solpar.GcdFlag
        0,	# areaInterchangeAdjustment, 
        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
        0,  # reorder (in dypar default = 0)
        )
print("*** Solution Result: %d" % errorCode)

"""
Results: Seems to solve, even with tapAdj, SVD, and phase shifters on.
* Next: Try changing islanded load/gen to cause divergence???

Additionally
When loading/solving .sav:

Error compiling epcl program for dcmt model in ENTR
Error compiling epcl program for dcmt model in ENTR
Error compiling epcl program for vscdc model in ENTR

Unable to find buses will skip these records
check the rdydtemp.log file for detailed Error messages

Unable to find elements (gen,load)
check the rdydtemp.log file for detailed Error messages

Single change requires 11 iterations - doesn't account for slack error target...
double change requires 13 iterations - doesn't account for slack error target...

"""
