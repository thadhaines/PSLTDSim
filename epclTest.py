"""A standalone test of running EPCL commands to show code errors/crashes"""
# Python 3.6 with pythonnet

import clr
import sys
sys.path.append(r"C:\Program Files (x86)\GE PSLF")

#clr.AddReference(r"C:\Program Files (x86)\GE PSLF\PslfMiddleware") #pythonnet call
clr.AddReference("PslfMiddleware")
clr.AddReference("IronPython.Modules")
clr.AddReference("IronPython")
#clr.AddReference(r"C:\Program Files (x86)\GE PSLF\PslfEngine") #pythonnet call
#clr.AddReferenceToFileAndPath(r"C:\Program Files (x86)\GE PSLF\PslfMiddleware") #ironpython call
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col
import System

pslfPath = r"C:\Program Files (x86)\GE PSLF"
savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"

PSLF = mid.Pslf(pslfPath)
PSLF.LoadCase(savPath)
PSLF.SolveCase()
PSLF.RunEpcl("dispar[0].noprint = 1") # turn off terminal solution details

n=0
limit = 1549-1 # crash limit changes per computer memory setup
Pload = 0.01

load = col.LoadDAO.FindByBusIndexAndId(4, '1')
print(load)
#id = load.__idx
id = 0
pythonP = load.P


# Funtion usage that crashes:
print(load.P)
load.P += 666
print("changing load to 666 and attempting save.")
try:
    load.Save()
except System.NotImplementedException:
    print("caught...")
load = col.LoadDAO.FindByBusIndexAndId(4, '1')
print(load.P)
# Workaround that also eventually crashes
epclTest = ("load[%d].p = load[%d].p + %f" % (id,id,Pload))
while n < limit:
    n+=1
    #PSLF.RunEpcl("dispar[0].noprint = 1") # also crashes if this is ran instead
    PSLF.RunEpcl(epclTest)
    pythonP += Pload
    pslfP = col.LoadDAO.FindByBusIndexAndId(4, '1').P
    print("%d\tpy %.4f\t ge %.4f" %(n, pythonP, pslfP))