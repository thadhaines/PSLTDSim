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
        self.Branch = []
        self.Gens = []
        self.Load = []
        self.Slack = []
        self.Machines = []
        self.PowerPlant = []
        self.Bus = []
        self.Shunt = []
        self.Timer ={}
        self.BA = None
        self.AreaSlack = None
        #self.SVD = []

        # Current Timestep values
        self.cv={
            'Pe' : 0.0,
            'Pm' : 0.0,
            'P' : 0.0, # Load
            'Q' : 0.0, # Load
            'SCEsum' : 0.0, # maybe not useful
            'IC0' : 0, # scheduled interchange
            'IC' :0,    # current area interchange
            'ICerror' :0,
            }

        #Area Frequency response Characteristic
        self.beta = 0.0

        # Init Interchange in IPY
        self.initIC()

    def getPref(self):
        """Return reference to PSLF object"""
        return col.AreaDAO.FindByAreaNumber(self.Area) # untested....

    def getPvals(self):
        """Get most recent PSLF values"""
        pObj = self.getPref()
        self.cv['IC'] = float(pObj.Pnet)

    def setPvals(self):
        """Set PSLF values"""
        # areas have nothing to set
        pass

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Area',
               'AreaNum':self.Area,
               'IC': self.cv['IC'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['IC'] = msg['IC']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def sumSCE(self):
        """ Sum station control error in area """
        #NOTE: Not really station control error -Unused 9/20/2019
        self.cv['SCEsum'] = 0.0
        for mach in self.Machines:
            self.cv['SCEsum'] += mach.cv['SCE']

    def calcICerror(self):
        """ Calculate Interchange Error """
        #self.cv['IC'] = self.cv['Pe'] - self.cv['P'] # should be repopulated every step by AMQP
        self.cv['ICerror'] = self.cv['IC'] - self.cv['IC0']

    def initIC(self):
        """ Initiate Interchange Value (if <0, Importing Power)"""
        #self.cv['IC'] = self.cv['Pe'] - self.cv['P']
        #self.cv['IC0'] = self.cv['IC']
        pRef = self.getPref()
        self.cv['IC0'] = float(pRef.Pnet)
        self.cv['IC'] = self.cv['IC0']

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

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Pe = [0.0]*self.mirror.dataPoints
        self.r_Pm = [0.0]*self.mirror.dataPoints
        self.r_P = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints
        self.r_SCEsum = [0.0]*self.mirror.dataPoints
        self.r_IC = [0.0]*self.mirror.dataPoints
        self.r_ICerror = [0.0]*self.mirror.dataPoints
        self.r_Losses = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Put current values into log"""
        n = self.mirror.cv['dp']
        self.r_Pe[n] = self.cv['Pe']
        self.r_Pm[n] = self.cv['Pm']
        self.r_P[n] = self.cv['P']
        self.r_Q[n] = self.cv['Q']
        self.r_SCEsum[n] = self.cv['SCEsum']
        self.r_IC[n] = self.cv['IC']
        self.r_ICerror[n] = self.cv['ICerror']
        self.r_Losses[n] = self.cv['Pe']-self.cv['P']-self.cv['IC']


    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_P = self.r_P[:N]
        self.r_Q = self.r_Q[:N]
        self.r_SCEsum = self.r_SCEsum[:N]
        self.r_IC = self.r_IC[:N]
        self.r_ICerror = self.r_ICerror[:N]
        self.r_Losses[n] = self.r_Losses[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'AreaNum': self.Area,
             'Ngen': self.Ngen,
             'Nload': self.Nload,
             'Pe' : self.r_Pe,
             'Pm' : self.r_Pm,
             'P' : self.r_P,
             'Q' : self.r_Q,
             'beta' : self.beta,
             'SCEsum' : self.r_SCEsum,
             'IC' : self.r_IC,
             'ICerror' : self.r_ICerror,
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


