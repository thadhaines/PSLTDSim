"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

# Required Paths
## full path to dll
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  
## path to folder containing PSLF license
pslfPath = r"C:\Program Files (x86)\GE PSLF"  
## .sav path
savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
#savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
#savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
## .dyd path
dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"
#dydPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"
#dydPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"
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
mirror = Model(locations, 0, 1)

# testing of information display functions
mirror.dispCP()
mirror.sumPower()
mirror.dispPow()

# Check should be included n default model init behavior
for x in range(mirror.Narea):
    mirror.Area[x].checkArea()

print("Current dir():")
print(dir())

# to view size of mirror
import sys 
print("mirror size [bytes]: %d " % sys.getsizeof(mirror))

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
#raw_input("Press <Enter> to Continue. . . . ")