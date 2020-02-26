""" 
IPY only simulation - Often via interactive run
Used to verify hard trip behavior as you keep using that word, 
but it may not mean what you think it means
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
#os.chdir(r"C:\Users\thad\source\repos\thadhaines\PSLTDSim")
os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")

print(os.getcwd())

ltd.terminal.dispCodeTitle()

# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    'savPath' : r"C:\LTD\pslf_systems\sixMachine\sixMachine.sav",
    'dydPath':  [r"C:\LTD\pslf_systems\sixMachine\sixMachine.dyd"], # note that this is a list
    'ltdPath': None,
    }

### Start Simulation functions calls
ltd.init_PSLF(locations)

import time
__builtin__.time = time

# PSLF initialized with supplied Case

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

## Soft Trip gen 5
# locate gen 5 vis PSLF IPY API
a2gens = col.GeneratorDAO.FindByArea(2)
g5 = None
for gen in a2gens:
    if gen.GetBusNumber() == 5:
        g5 = gen
        break

# Display current P, Qmin, Qmax
print(g5)
print("State\t %2.f" % g5.St)
print("Pgen\t %2.f" % g5.Pgen)
print("Qgen\t %2.f" % g5.Qgen)
print("Qmax\t %2.f" % g5.Qmax)
print("Qmin\t %2.f" % g5.Qmin)

# Change State
g5.St = 0
# Save Changes to PSLF
g5.Save()


# Verify Changes correctly saved
# Collect from PSLF again
a2gens = col.GeneratorDAO.FindByArea(2)
g5 = None
for gen in a2gens:
    if gen.GetBusNumber() == 5:
        g5 = gen
        break

# Display current P, Qmin, Qmax
print(g5)
print("State\t %2.f" % g5.St)
print("Pgen\t %2.f" % g5.Pgen)
print("Qgen\t %2.f" % g5.Qgen)
print("Qmax\t %2.f" % g5.Qmax)
print("Qmin\t %2.f" % g5.Qmin)

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

# Verify Changes observed after solve
# Collect from PSLF again
a2gens = col.GeneratorDAO.FindByArea(2)
g5 = None
for gen in a2gens:
    if gen.GetBusNumber() == 5:
        g5 = gen
        break

# Display current P, Qmin, Qmax
print(g5)
print("State\t %2.f" % g5.St)
print("Pgen\t %2.f" % g5.Pgen)
print("Qgen\t %2.f" % g5.Qgen)
print("Qmax\t %2.f" % g5.Qmax)
print("Qmin\t %2.f" % g5.Qmin)

"""
Results: 
As suddenly realized, a hard trip doesn't change any PSLF table values to zero.
This behavior is more than likely causing issues with trips.
Therefore, as any addict could probably have guessed, soft trips > hard trips.
"""
