"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

# workaround for interactive mode runs
import os
print(os.getcwd())
# os.chdir("C:\\Users\\thad\\Source\\Repos\\thadhaines\\LTD_sim\\")

# Required Paths
## full path to dll
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

execfile('CoreAgents.py')
execfile('Model.py')

# mirror arguments: locations, Htot, debug NOTE: will probably change
mirror = Model(locations, 0, 0)

# testing of information display functions
mirror.dispCP()
mirror.sumPower()
mirror.dispPow()

# Check should be included n default model init behavior
for x in range(mirror.Narea):
    mirror.Area[x].checkArea()

# Display 'workspace' variables
print("Current dir():")
print(dir())

# View size of mirror (may matter in future)
import sys 
print("mirror size [bytes]: %d " % sys.getsizeof(mirror))

# Verification of H parsing
htot = 0
for x in range(len(mirror.PSLFdynamics)):
    print("%.2f on Busnum %d " % (mirror.PSLFdynamics[x].H, mirror.PSLFdynamics[x].Busnum))
    htot +=mirror.PSLFdynamics[x].H

print("System H: %.3f" % htot)
htot = 0
for x in range(len(mirror.Machines)):
    print("%.2f on Busnum %d " % (mirror.Machines[x].H, mirror.Machines[x].Busnum))
    htot+=mirror.Machines[x].H

print("System H: %.3f" % htot)
print("Non PU H = %.3f " % mirror.ss_H)


# Find any dyd and .sav mbase varience
print("***Test of Mbase model agreement***")
mismatch = 0
for x in range(len(mirror.Machines)):
    savMbase = mirror.Machines[x].Mbase
    dydMbase = mirror.Machines[x].machine_model[0].Mbase
    if savMbase != dydMbase:
        mismatch = 1
        print("Gen on Bus %d has Mbase mismatch:" % mirror.Machines[x].Busnum)
        print("sav %.3f" % mirror.Machines[x].Mbase)
        print("dyd %.3f" % mirror.Machines[x].machine_model[0].Mbase)

if mismatch == 0:
    print("Mbase in sav and dyd are in agreement.")
raw_input("Press <Enter> to Continue. . . . ")