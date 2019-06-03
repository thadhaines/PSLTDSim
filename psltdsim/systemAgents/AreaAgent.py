class AreaAgent(object):
    """Area Agent for LTD mirror Collections"""

    def __init__(self, mirror, areaNum):
        # mirror Reference
        self.mirror = mirror

        # Identification
        self.Area = areaNum

        # Case Parameters
        self.Ngen = len(col.GeneratorDAO.FindByArea(self.Area))
        self.Nload = len(col.LoadDAO.FindByArea(self.Area))
        self.Nbranch = len(col.BranchDAO.FindByArea(self.Area))
        self.Nshunt = len(col.ShuntDAO.FindByArea(self.Area))
        #self.Nxfmr = len(col.BranchDAO.FindByArea(self.Area))

        # Children
        self.Gens = []
        self.Load = []
        self.Slack = []
        self.Machines = []
        self.Bus = []
        self.Shunt = []
        self.Branch = []
        self.SVD = []
        self.AreaSlack = None

        # Current Timestep values
        self.Pe = 0.0
        self.Pm = 0.0
        self.P = 0.0
        self.Q = 0.0

        #TODO: Add mor ACE variables?
        self.beta = 0.0

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Pe = [0.0]*self.mirror.dataPoints
        self.r_Pm = [0.0]*self.mirror.dataPoints
        self.r_P = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Put current values into log"""
        self.r_Pe[self.mirror.c_dp] = self.Pe
        self.r_Pm[self.mirror.c_dp] = self.Pm
        self.r_P[self.mirror.c_dp] = self.P
        self.r_Q[self.mirror.c_dp] = self.Q

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_P = self.r_P[:N]
        self.r_Q = self.r_Q[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'AreaNum': self.Area,
             'Ngen': self.Ngen,
             'Nload': self.Nload,
             'Pe' : self.r_Pe,
             'Pm' : self.r_Pm,
             'P' : self.r_P,
             'Q' : self.Q,
             }
        return d

    def checkArea(self):
        """Checks if found number of Generators and loads is Correct
        Creates Machine list
        Returns 0 if all valid
        """
        # Q: check for SVD ?
        self.Machines = self.Slack + self.Gens

        if self.Ngen == (len(self.Machines)):
            if self.mirror.debug: 
                print("Gens correct in Area:\t%d" % self.Area)
        else:
            print("*** Gen Error: %d/%d found. Area:\t%d" % 
                  (len(self.Machines), self.Ngen, self.Area))
            return -1

        if self.Nload == len(self.Load):
            if self.mirror.debug: 
                print("Load correct in Area:\t%d" % self.Area)
        else:
            print("*** Load Error: %d/%d found. Area:\t%d" % 
                  (len(self.Load), self.Nload, self.Area))
            return -2

        if self.Nshunt == len(self.Shunt):
            if self.mirror.debug: 
                print("Shunts correct in Area:\t%d" % self.Area)
        else:
            print("*** Shunt Error: %d/%d found. Area:\t%d" % 
                  (len(self.Shunt), self.Nshunt, self.Area))
            return -3

        if self.Nbranch== len(self.Branch):
            if self.mirror.debug: 
                print("Branches correct in Area:\t%d" % self.Area)
        else:
            print("*** Branch Error: %d/%d found. Area:\t%d" % 
                  (len(self.Branch), self.Nbranch, self.Area))
            return -4

        return 0

    def calcBeta(self):
        """Calculate Beta (area frequency response characteristic)"""
        self.beta = 0.0
        #for each machine
        for mach in self.Machines:
            #if machine has a gov
            if mach.gov_model:
                # convert droops to system base
                Rnew = mach.gov_model.R*self.mirror.Sbase/mach.gov_model.Mbase
                #sum 1/droop
                self.beta += 1.0/Rnew
