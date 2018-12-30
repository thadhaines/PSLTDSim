"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

# workaround for interactive mode runs
import os
print(os.getcwd())
# os.chdir("C:\\Users\\thad\\Source\\Repos\\thadhaines\\LTD_sim\\")

# Simulation Parameters
timeStep = 1.0
endTime = 10.0
slackTol = 1.0
Hsys = 0.0 # MW*sec of entire system, if !> 0.0, will be calculated
Dsys = 0.0 # PU - more of a placeholder

# Required Paths
## full path to middleware dll
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  
## path to folder containing PSLF license
pslfPath = r"C:\Program Files (x86)\GE PSLF"  

test_case = 2
if test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"
elif test_case == 3:
    """Will no longer run due to parser errors"""
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )
del fullMiddlewareFilePath, pslfPath, savPath, dydPath

simParams = (
    timeStep,
    endTime,
    slackTol,
    Hsys,
    Dsys,
    )
del timeStep, endTime, slackTol, Hsys, Dsys

# these files will change after refactor
execfile('CoreAgents.py')
execfile('Model.py')

# mirror arguments: locations, simParams, debug flag
mirror = Model(locations, simParams, 0)

# testing of information display functions
mirror.dispCaseP()
mirror.sumPower()
mirror.dispPow()

# Display 'workspace' variables
print("Current dir():")
print(dir())

# View size of mirror (may matter in future)
import sys 
print("mirror size [bytes]: %d " % sys.getsizeof(mirror))

# Verification of H parsing
htot = 0
for x in range(len(mirror.Machines)):
    print("%.2f on Busnum %d " % (mirror.Machines[x].H, mirror.Machines[x].Busnum))
    htot+=mirror.Machines[x].H

print("Summed System H [MW*sec] = %.3f " % htot)
print("System H [MW*sec] = %.3f " % mirror.Hsys)


# Find any dyd and .sav mbase varience
print("***Test of Mbase model agreement***")
mismatch = 0
for x in range(len(mirror.Machines)):
    savMbase = mirror.Machines[x].MbaseSAV
    dydMbase = mirror.Machines[x].MbaseDYD
    if savMbase != dydMbase:
        mismatch = 1
        print("Gen on Bus %d has Mbase mismatch:" % mirror.Machines[x].Busnum)
        print("sav %.3f" % mirror.Machines[x].MbaseSAV)
        print("dyd %.3f" % mirror.Machines[x].machine_model[0].Mbase)

if mismatch == 0:
    print("Mbase in sav and dyd are in agreement.")

raw_input("Press <Enter> to Continue. . . . ")