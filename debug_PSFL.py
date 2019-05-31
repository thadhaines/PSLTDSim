""" IPY only - Loads Case into PSLF 
Used to interactively explore middleware capabilities
"""

import os
import subprocess
import signal
import time
import __builtin__

# import custom package and make truly global
import psltdsim as ltd
__builtin__.ltd = ltd

print(os.getcwd())

# workaround for interactive mode runs (Use as required)
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
#print(os.getcwd())
"""
savPath = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1.dyd"]

savPath = r"C:\LTD\pslf_systems\fullWecc\16HS\16HS3a.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\16HS\16HS31_dg.dyd"]
"""



#savPath = r"C:\LTD\pslf_systems\fullWecc\14LS_DE\14LS_100GW_ALS_SHAWN.sav"
#dydPath = [r"C:\LTD\pslf_systems\fullWecc\14LS_DE\14ls11e_21P1a_dg.dyd"]

savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"]

ltdPath = None


debug = 1
simNotes = """
none
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.25,
    'endTime': 1.5,
    'slackTol': 1.0,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; TODO: Incoroporate into simulation (probably)

    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'euler',

    # Data Export Parameters
    'fileDirectory' : "\\verification\\miniWeccTest01\\", # relative path must exist before simulation
    'fileName' : 'miniWECC_loadStep06IPY',

    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

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

ltd.init_PSLF(locations, False)

# Attempt to find Global Slack
# Assumes global slack = area slack of area with most buses.... 
# Apparently not always the case.
areaD = {}
maxBus = 0
maxBusArea = 0

for area in range(col.AreaDAO.FindNextAvailableAreaNumber()):
    nBus = len(col.AreaDAO.FindBusesInArea(area))
    if nBus > 0:
        areaD[str(area)] = len(col.AreaDAO.FindBusesInArea(area))

    if nBus > maxBus:
        maxBus = nBus
        maxBusArea = col.AreaDAO.FindByAreaNumber(area)

print("Area with most buses is Area {}".format(maxBusArea))
sa = maxBusArea

swingMW = maxBusArea.Swingmw
swingPMax = maxBusArea.Swingpmax
found = False

## Attempt to locate global slack by mw and pmax.
# collect all gens in area
areaGens = col.GeneratorDAO.FindByArea(maxBusArea.Arnum)
# for each generator, get bus number,
for gen in areaGens:
    genBusNum = gen.GetBusNumber()
    bus = col.BusDAO.FindFirstBusByNumber(genBusNum)

    # check if bus is slack type
    if bus.Type == 0:
        print(gen.Pmax)
        # for each slack check mw and pmax tol from expected....
        if gen.Pmax == swingPMax:
            print('swingPMax match...')
            if gen.Pgen == swingMW:
                globalSlack = gen
                found = True

    if found:
        break
if found:
    print("Global Slack is: {} on bus {}".format(globalSlack.GetBusName(),globalSlack.GetBusNumber()))
else:
    print('No findy find... :(')
    print(swingPMax)

## Second attempt with more familiarity...
# Finds bus with area slack attached
areaSwingBus = {}
maxBus = 0
maxBusArea = 0

for area in range(col.AreaDAO.FindNextAvailableAreaNumber()):
    nBus = len(col.AreaDAO.FindBusesInArea(area))
    if nBus > 0:
        areaObj = col.AreaDAO.FindByAreaNumber(area)
        areaSwingBus[str(area)] = col.BusDAO.FindByIndex(areaObj.Iswng)

    if nBus > maxBus:
        maxBus = nBus
        maxBusArea = col.AreaDAO.FindByAreaNumber(area)

print("Area with most buses is Area {}".format(maxBusArea))
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(areaSwingBus)