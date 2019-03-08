class GeneratorAgent(object):
    """Generator Agent for LTD Model"""
    def __init__(self, model, parentBus, newGen):
        # Model/Parent Reference
        self.model = model
        self.Bus = parentBus

        # Identification 
        self.Id = newGen.Id
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.Zone = newGen.Zone
        self.Busnam = newGen.GetBusName()
        self.Busnum = newGen.GetBusNumber()
        self.Scanbus = newGen.GetScanBusIndex()

        # Characteristic Data
        self.MbaseSAV = float(newGen.Mbase)
        self.MbaseDYD = 0.0
        self.H = 0.0
        self.Hpu = 0.0
        self.Pmax = float(newGen.Pmax)
        self.Qmax = float(newGen.Qmax)

        # Q: Should Vsched = self.Bus.Vsched? seems better utilized in PSLF
        self.Vsched = float(newGen.Vcsched) # This value seems unused in PSLF

        # Current Status
        self.St = int(newGen.St)
        self.IRP_flag = 1       # Inertia response participant flag
        self.Pe = float(newGen.Pgen)   # Generated Power
        self.Pm = self.Pe       # Initialize as equal
        self.Q = float(newGen.Qgen)    # Q generatred       
        
        # History 
        self.r_Pm = [0.0]*model.dataPoints
        self.r_Pe = [0.0]*model.dataPoints
        self.r_Q = [0.0]*model.dataPoints
        self.r_St = [0.0]*model.dataPoints

        # Children
        self.machine_model = []
        # TODO: implement proportional governor
        self.gov = []
        self.exc = None
        
    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.GeneratorDAO.FindByBusIndexAndId(self.Scanbus,self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pRef = self.getPref()
        self.Pe = float(pRef.Pgen)
        self.Q = float(pRef.Qgen)
        self.St = int(pRef.St)

    def setPvals(self):
        """Send current mirror values to PSLF"""
        pRef = self.getPref()
        pRef.Pgen = self.Pe
        pRef.St = self.St
        pRef.Save()
        # pythonnet workaround: Replace save with EPCL
        #sb = str(self.Scanbus)
        
        #pStr = ("gens[%s].pgen = %f\n" %(sb,self.Pe))
        #PSLF.RunEpcl(pStr)
        #stStr = ("gens[%s].st = %d\n" %(sb,self.St))
        #PSLF.RunEpcl( pStr + stStr)


    def logStep(self):
        """Step to record log history"""
        self.getPvals()
        self.r_Pe[self.model.c_dp] = self.Pe
        self.r_Pm[self.model.c_dp] = self.Pm
        self.r_Q[self.model.c_dp] = self.Q
        self.r_St[self.model.c_dp] = self.St

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_Q  =self.r_Q[:N]
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Q': self.r_Q,
             'St': self.r_St,
             'Mbase' : self.MbaseDYD,
             'Hpu' : self.Hpu,
             'Slack' : 0,
             }
        return d