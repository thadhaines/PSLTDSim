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

        # Case Parameters
        self.Nload = len(col.LoadDAO.FindByBus(self.Scanbus))
        self.Ngen = len(col.GeneratorDAO.FindByBus(self.Scanbus))

        # Children
        self.Gens = []
        self.Slack = []
        self.Load = []

        # if this is how shunts/SVDs work...
        self.Shunt = []
        self.SVD = []

        # Current Status
        self.Vm = newBus.Vm     # Voltage Magnitude
        self.Va = newBus.Va     # Voltage Angle (radians)

        # Voltage settings
        #self.Vmax = newBus.Vmax # These values don't seem to be always set
        #self.Vmin = newBus.Vmin
        self.Vsched = float(newBus.Vsched)

        # History
        self.r_Vm = [0.0]*self.model.dataPoints
        self.r_Va = [0.0]*self.model.dataPoints

    def __str__(self):
        """Possible useful identification function"""
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Extnum).zfill(3), self.Busnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.BusDAO.FindByIndex(self.Scanbus)

    def getPvals(self):
        """Get most recent PSLF values"""
        pObj = self.getPref()
        self.Vm = pObj.Vm
        self.Va = pObj.Va

    def setPvals(self):
        """Set PSLF values"""
        pObj = self.getPref()
        pObj.Vm = self.Vsched
        pObj.Save()
        # pythonnet workaround Save() -> RunEplc
        #sb = str(self.Scanbus)
        #vmStr = ('volt[%s].vm = %f' % (sb, self.Vsched))
        #PSLF.RunEpcl(vmStr)

    def logStep(self):
        """Put current values into log"""
        self.getPvals()
        self.r_Vm[self.model.c_dp] = self.Vm
        self.r_Va[self.model.c_dp] = self.Va

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Vm = self.r_Vm[:N]
        self.r_Va = self.r_Va[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Vm': self.r_Vm,
             'Va': self.r_Va,
             'BusName': self.Busnam,
             'BusNum': self.Extnum,
             }
        return d