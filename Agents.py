"""LTD Agent File"""
from __main__ import *

# Bus Creation
class Bus(object):
    """Bus Agent for LTD Model"""
    def __init__(self, newBus):
        # Identification 
        self.Area = newBus.Area
        self.Busnam = newBus.Busnam
        self.Extnum = newBus.Extnum
        self.Scanbus = newBus.GetScanBusIndex()
        self.Type = newBus.Type

        # Current Status
        self.Vm = newBus.Vm     # Voltage Magnitude
        self.Va = newBus.Va     # Voltage Angle (radians)

        # Children
        self.Nload = len(col.LoadDAO.FindByBus(self.Extnum))
        self.Ngen = 0
        self.gen = []
        self.load = []

    def __str__(self):
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def getPval(self):
        """Get most recent PSLF values"""
        pObj = col.BusDAO.FindByIndex(self.Scanbus)
        self.Vm = pObj.Vm
        self.Va = pObj.Va

##
# Generator Class
class Generator(object):
    """Generator Agent for LTD Model"""
    def __init__(self, newGen):
        # Identification 
        self.Id = newGen.Id
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.Zone = newGen.Zone
        self.Busnam = newGen.GetBusName()
        self.Busnum = newGen.GetBusNumber()
        self.Scanbus = newGen.GetScanBusIndex()
        self.Mbase = newGen.Mbase

        # Current Status
        self.Pm = newGen.Pgen   # Voltage Magnitude
        self.Pe = self.Pm       # Initialize as equal
        self.Q = newGen.Qgen    # Q generatred

        # the idea is to have current status variables, then move that to a time sequence list at each step

        # Children
        self.dynamics = []