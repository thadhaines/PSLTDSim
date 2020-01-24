""" IPY only simulation - Used to experiment with possibilities of transformer agent
"""

import os
import subprocess
import signal
import time
import __builtin__

print(os.getcwd())
# Point to main PSLTDSim folder
# workaround for interactive mode runs (Use as required)
#os.chdir(r"C:\Users\heyth\source\repos\thadhaines\PSLTDSim")
os.chdir(r"C:\Users\thad\source\repos\thadhaines\PSLTDSim")
#os.chdir(r"D:\Users\jhaines\source\Repos\thadhaines\PSLTDSim")
print(os.getcwd())

# import custom package and make truly global
import psltdsim as ltd
__builtin__.ltd = ltd

ltd.terminal.dispCodeTitle()


# Required Paths Dictionary
locations = {
    # path to folder containing middleware dll
    'middlewareFilePath': r"C:\Program Files (x86)\GE PSLF\PslfMiddleware" ,
    # path to folder containing PSLF license
    'pslfPath':  r"C:\Program Files (x86)\GE PSLF",
    #'savPath' : r"C:\LTD\pslf_systems\sixMachine\sixMachineTrips.sav",
    #'dydPath':  [r"C:\LTD\pslf_systems\sixMachine\sixMachine.dyd"], # note that this is a list
    'savPath' : r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav",
    'dydPath':  [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTD.dyd"], # note that this is a list
    'ltdPath': None,
    }

### Start Simulation functions calls
ltd.init_PSLF(locations)

import time
__builtin__.time = time

# PSLF initialized with case (unless otherwise noted)

### End of `generic IPY' init ###

#t1 = col.TransformerDAO.FindByAnyBus(0)[0] # find xfmr on bus index 1, sixMachine
t1 = col.TransformerDAO.FindByAnyBus(62)[1] # find xfmr on bus index 63-95, miniWECC
"""
for item in dir(t1):
    val = eval('t1.'+item)
    print('%s\t%s' % (item, str(val) )) # print all attributes of transformer
"""

St = t1.St # status
Ck = t1.Ck
Area = t1.Area
sortNDX = t1._Idx
X = t1.Zpsx # X
R = t1.Zpsr # R

# get external from bus number
busName = t1.GetBusName()
busKv = t1.GetBusBasekv()
busNum = t1.GetBusNumber()
Bus = col.BusDAO.FindBusByNumberNameKv(busNum, busName, busKv)
print(Bus.Extnum)

# get external to bus number
TbusName = t1.GetToBusName()
TbusKv = t1.GetToBusBasekv()
TbusNum = t1.GetToBusNumber()
TBus = col.BusDAO.FindBusByNumberNameKv(TbusNum, TbusName, TbusKv)
print(TBus.Extnum)

# Locate xfmr in PSLF using collected values (required for future updates)
t2 = col.TransformerDAO.FindByIndex(sortNDX)
print(t1 == t2)

areas = [1,2,3]
totXFMR  = 0 
for area in areas:
    # collect transformers in area
    areaXFMR = col.TransformerDAO.FindByArea(area)
    # count transformers
    totXFMR += len(areaXFMR)

print("Total XFMRs = %d" % totXFMR)
"""
General idea: if St = 1
initialize transformer with idx, external bus numbers, and any R+jX values in IPY 
else pass

then in PY3
for each xfmr
link XFMR between known external bus numbers

each step
calculate power flows
log

Essentially a branch agent/ power flow logger
Issues predicted with caluclations as each side will be in a different voltage area
Compute in PU multiply by Sbase?
"""