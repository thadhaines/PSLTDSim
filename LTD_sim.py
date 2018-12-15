"""Developement file that acts as main"""

# Required Paths
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  # full path to dll
pslfPath = r"C:\Program Files (x86)\GE PSLF"  # path to folder containing PSLF license
savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )
del fullMiddlewareFilePath, pslfPath, savPath, dydPath

execfile('CoreAgents.py')
execfile('Model.py')

env = Model(locations, 0, 1) # locations, Htot, debug
env.dispCP()

for x in range(env.Narea):
    env.Area[x].checkArea()

print("Current dir():")
print(dir())

import sys # to view size of env
print("mirror size [bytes]: %d " % sys.getsizeof(env))
raw_input("Press <Enter> to Continue. . . . ")