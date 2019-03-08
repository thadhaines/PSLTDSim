class LoadAgent(object):
    """Load Agent for LTD Model"""
    def __init__(self,model, parentBus, newLoad):
        # Model/Parent Reference
        self.model = model
        self.Bus = parentBus

        # Identification
        self.Id = newLoad.Id
        self.Area = newLoad.Area
        self.Zone = newLoad.Zone

        # Current Status
        self.P = float(newLoad.P)
        self.Q = float(newLoad.Q)
        self.St = int(newLoad.St)

        # History 
        self.r_P = [0.0]*model.dataPoints
        self.r_Q = [0.0]*model.dataPoints
        self.r_St = [0.0]*model.dataPoints

        # dynamics?

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Bus.Extnum).zfill(3), self.Bus.Busnam)

        return(tag1+tag2)


    def getPref(self):
        """Return reference to PSLF object"""
        return col.LoadDAO.FindByBusIndexAndId(self.Bus.Scanbus, self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pRef = self.getPref()
        self.P = float(pRef.P)
        self.Q = float(pRef.Q)
        self.St = int(pRef.St)

    def logStep(self):
        """Step to record log history"""
        self.r_P[self.model.c_dp] = self.P
        self.r_Q[self.model.c_dp] = self.Q
        self.r_St[self.model.c_dp] = self.St

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_P = self.r_P[:N]
        self.r_Q = self.r_Q[:N]
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'P': self.r_P,
             'Q': self.r_Q,
             'St': self.r_St,
             }
        return d