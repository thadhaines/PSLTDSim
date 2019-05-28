class Mirror(object):
    """Mirror class used as LTD system environment"""

    def __init__(self, locations, simParams, simNotes=None, debug = 0, AMQPdebug =0):
        """Carries out initialization of Mirror and meta data"""
        global PSLF
        from datetime import datetime
        init_start = time.time()
        __module__= "Mirror"

        # Model Meta Data
        self.created = datetime.now()
        self.simNotes = simNotes

        # Solution timing information
        self.SimTime = 0.0
        self.DynamicTime = 0.0
        self.PFTime = 0.0
        self.PFSolns = 0
        self.PY3msgs = 0
        self.IPYmsgs = 0
        self.IPYmsgMake = 0.0
        self.IPYSendTime = 0.0
        self.IPYdistPaccTime = 0.0
        self.IPYPvalsTime = 0.0
        self.PY3SendTime = 0.0
        self.PY3RecTime = 0.0
        self.FindTime = 0.0
        self.IPYFindTime = 0.0

        # Simulation Parameters from User
        self.simParams = simParams
        self.locations = locations
        self.timeStep = simParams['timeStep']
        self.endTime = simParams['endTime']
        self.slackTol = simParams['slackTol']
        self.Hinput = simParams['Hsys']
        self.Dinput = simParams['Dsys']
        self.debug = debug
        self.AMQPdebug = AMQPdebug
        self.dataPoints = int(self.endTime//self.timeStep + 1) # add extra points here...

        # Simulation Variable Prefix Key
        # c_ ... current
        # ss_ .. system sum
        # r_ ... running (time series)

        # Varaible initalization
        self.c_dp = 0 # current data point
        self.c_t = 0.0

        self.c_f = 1.0
        self.c_fdot = 0.0
        self.c_deltaF = 0.0

        self.ss_H = 0.0 # placeholder, Hsys used in maths

        self.ss_Pe = 0.0
        self.ss_Pm = 0.0
        self.ss_Pacc = 0.0

        self.ss_Qgen = 0.0
        self.ss_Qload = 0.0
        self.ss_Pload = 0.0

        self.ss_Pert_Pdelta = 0.0
        self.ss_Pert_Qdelta = 0.0

        # Agent Collections
        self.Area = []
        self.Bus = []
        self.Gens = []
        self.Load = []
        self.Slack = []
        self.Perturbance = []
        self.Dynamics = []
        self.Shunt = []
        self.Branch = []

        # initial system solve
        try:
            ltd.mirror.LTD_SolveCase(self)
        except ValueError as e:
                print("*** Error Caught")
                print(e)

        # Initialize mirror with PSLF values
        self.Ngen = PSLF.GetCasepar('Ngen')
        self.Nbus = PSLF.GetCasepar('Nbus')
        self.Nload = PSLF.GetCasepar('Nload')
        self.Narea = PSLF.GetCasepar('Narea')
        self.Nzone = PSLF.GetCasepar('Nzone')
        self.Nbrsec = PSLF.GetCasepar('Nbrsec')
        self.Nshunt = PSLF.GetCasepar('Nshunt')
        self.Sbase = float(PSLF.GetCasepar('Sbase'))

        # initialize agents
        ltd.mirror.create_mirror_agents(self)
        ltd.mirror.findGlobalSlack(self)

        # Combined Collections
        self.Machines = self.Slack + self.Gens

        # TODO: As logging capability added to agents, add to Log collection
        self.Log = [self] + self.Load + self.Bus + self.Machines + self.Area

        # Check mirror accuracy in each Area, create machines list for each area
        for c_area in range(self.Narea):
            if self.debug: print("*** Verifying area data...")
            valid = self.Area[c_area].checkArea()
            if valid != 0:
                print("Mirror inaccurate in Area %d, error code: %d" % (c_area, valid))

        # init_dynamics
        self.PSLFmach = []
        self.PSLFgov = []
        
        # read dyd, create pslf models
        if locations['ltdPath']:
            dydPaths = locations['dydPath'] + locations['ltdPath']
        else:
            dydPaths = locations['dydPath']

        ltd.parse.parseDyd(self, dydPaths)

        # parse LTD to handly ltd models and perturbances
        # Moved to begining of runSimPY3 -> IPY mirror doesn't need ltd info
        #if locations['ltdPath']:
        #    ltd.parse.parseLtd(self, locations['ltdPath'])

        # ensure dyd changes reflected in mirror (i.e. mbase, mwcap)
        for gov in self.PSLFgov:
            gov.Gen.Pmax = gov.mwCap

        # link H and mbase to mirror
        ltd.mirror.initInertiaH(self)

        # Handle user input system inertia
        # NOTE: H is typically MW*sec unless noted as PU or in PSLF models
        if self.Hinput > 0.0:
            self.Hsys = self.Hinput
        else:
            self.Hsys = self.ss_H

        # calculate beta for each area NOTE: Nothing happends because dynamics not yet init..
        #for c_area in self.Area:
        #    c_area.calcBeta()

        init_end = time.time()
        self.InitTime = init_end-init_start
        print("*** Python Mirror intialized.")

    # Simulation Methods
    def initRunningVals(self):
        """Initialize History Values of mirror agent"""
        # initialize running (history) values 
        self.r_t = [0.0]*self.dataPoints

        self.r_f = [0.0]*self.dataPoints
        self.r_deltaF = [0.0]*self.dataPoints
        self.r_fdot = [0.0]*self.dataPoints

        self.r_ss_Pe = [0.0]*self.dataPoints
        self.r_ss_Pm = [0.0]*self.dataPoints
        self.r_ss_Pacc = [0.0]*self.dataPoints
        self.r_Pacc_delta = [0.0]*self.dataPoints

        self.r_ss_Qgen = [0.0]*self.dataPoints
        self.r_ss_Qload = [0.0]*self.dataPoints
        self.r_ss_Pload = [0.0]*self.dataPoints

        # for fun stats, not completely utilized - yet
        self.PLosses = 0.0
        self.QLosses = 0.0
        self.r_PLosses = [0.0]*self.dataPoints
        self.r_QLosses = [0.0]*self.dataPoints

    def logStep(self):
        """Update Log information"""
        self.r_f[self.c_dp] = self.c_f
        self.r_fdot[self.c_dp] = self.c_fdot
        self.r_deltaF[self.c_dp] = self.c_deltaF

        self.r_ss_Pe[self.c_dp] = self.ss_Pe
        self.r_ss_Pm[self.c_dp] = self.ss_Pm
        self.r_ss_Pacc[self.c_dp] = self.ss_Pacc

        self.r_ss_Qgen[self.c_dp] = self.ss_Qgen
        self.r_ss_Qload[self.c_dp] = self.ss_Qload
        self.r_ss_Pload[self.c_dp] = self.ss_Pload

        self.r_PLosses[self.c_dp] = self.PLosses
        self.r_QLosses[self.c_dp] = self.QLosses

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_t = self.r_t[:N]
        self.r_f = self.r_f[:N]
        self.r_fdot = self.r_fdot[:N]
        self.r_deltaF = self.r_deltaF[:N]

        self.r_ss_Pe = self.r_ss_Pe[:N]
        self.r_ss_Pm = self.r_ss_Pm[:N]
        self.r_ss_Pacc = self.r_ss_Pacc[:N]

        self.r_ss_Qgen = self.r_ss_Qgen[:N]
        self.r_ss_Qload = self.r_ss_Qload[:N]
        self.r_ss_Pload = self.r_ss_Pload[:N]
    
        self.r_PLosses = self.r_PLosses[:N]
        self.r_QLosses = self.r_QLosses[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        dt = self.created
        dtStrYMD = str(dt.year)+'/'+str(dt.month).zfill(2) +'/'+str(dt.day)
        dtStrHMS = str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second).zfill(2)

        meta = { 'integrationMethod' : self.simParams['integrationMethod'],
                'fileName' : self.simParams['fileName'],
                'freqEffects' : self.simParams['freqEffects'],
                'locations' : self.locations,
                'created' : dtStrYMD+' at '+dtStrHMS,
                'simNotes' : self.simNotes,
            }

        d = {'t': self.r_t,
             'f': self.r_f,
             'fdot': self.r_fdot,
             'deltaF': self.r_deltaF,
             'N': self.c_dp,
             'Pe': self.r_ss_Pe,
             'Pm': self.r_ss_Pm,
             'Pacc': self.r_ss_Pacc,
             'Qgen': self.r_ss_Qgen,
             'Pload': self.r_ss_Pload,
             'Qload': self.r_ss_Qload,
             'Sbase' : self.Sbase,
             'Hsys' : self.Hsys,

             'meta' : meta,
             }
        return d

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Created from:  %s\n" %(self.locations['savPath'])
        created = str(self.created)
        tag3 = "Created on:    %s" %(created)

        return(tag1+tag2+tag3)
