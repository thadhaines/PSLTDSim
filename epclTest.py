"""A standalone test of running EPCL commands to show code errors/crashes"""
# Python 3.6 with pythonnet

import clr

clr.AddReference(r"C:\Program Files (x86)\GE PSLF\PslfMiddleware")
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col

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
id = load.__idx
pythonP = load.P

# Funtion usage that crashes:
#load.P += .01
#load.Save()

# Workaround that also eventually crashes
epclTest = ("load[%d].p = load[%d].p + %f" % (id,id,Pload))
while n < limit:
    n+=1
    PSLF.RunEpcl(epclTest)
    pythonP += Pload
    pslfP = col.LoadDAO.FindByBusIndexAndId(4, '1').P
    print("%d\tpy %.4f\t ge %.4f" %(n, pythonP, pslfP))