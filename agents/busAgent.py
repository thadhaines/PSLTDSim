"""LTD Bus Agent Definition
None of which are fully developed.
"""

class BusAgent(object):
    """Bus Agent for LTD Model"""
    def __init__(self, model, newBus):
        # Model Reference
        self.model = model

        # Identification 
        self.Area = newBus.Area
        self.Busnam = newBus.Busnam
        self.Extnum = newBus.Extnum
        self.Scanbus = newBus.GetScanBusIndex()
        self.Type = newBus.Type

        # Current Status
        self.Vm = newBus.Vm     # Voltage Magnitude
        self.Va = newBus.Va     # Voltage Angle (radians)
        
        # Case Parameters
        self.Nload = len(col.LoadDAO.FindByBus(self.Scanbus))
        self.Ngen = len(col.GeneratorDAO.FindByBus(self.Scanbus))

        # Children
        self.Gens = []
        self.Slack = []
        self.Load = []

    def __str__(self):
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def getPval(self):
        """Get most recent PSLF values"""
        pObj = col.BusDAO.FindByIndex(self.Scanbus)
        self.Vm = pObj.Vm
        self.Va = pObj.Va