"""
    NOTE: Refactor gameplan:
        1. Remove most-all methods from mirror
        2. Get links working to refactored library
        3. define AMQP operations
        4. split runsim into py3 and ipy parts
"""

class Mirror(object):
    """Mirror class used as LTD system environment"""

    def __init__(self, locations, simParams, debug = 0):
        """Carries out initialization of Mirror and meta data
        """
        global PSLF
        from datetime import datetime

        __module__= "Mirror"
        # Model Meta Data
        self.created = datetime.now()
        self.notes = """Notes"""

        # Simulation Parameters from User
        self.simParams = simParams
        self.locations = locations
        self.timeStep = simParams['timeStep']
        self.endTime = simParams['endTime']
        self.slackTol = simParams['slackTol']
        self.Hinput = simParams['Hsys']
        self.Dinput = simParams['Dsys']
        self.debug = debug
        self.dataPoints = int(self.endTime//self.timeStep + 1)

        # Simulation Variable Prefix Key
        # c_ ... current
        # ss_ .. system sum
        # r_ ... running (time series)

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

        # initial system solve
        try:
            ltd.mirror.LTD_SolveCase(self)
        except ValueError as e:
                print("*** Error Caught")
                print(e)

        # Initialize mirror system (environment)
        ## Collect Case Parameters from PSLF
        self.Ngen = PSLF.GetCasepar('Ngen')
        self.Nbus = PSLF.GetCasepar('Nbus')
        self.Nload = PSLF.GetCasepar('Nload')
        self.Narea = PSLF.GetCasepar('Narea')
        self.Nzone = PSLF.GetCasepar('Nzone')
        self.Nbrsec = PSLF.GetCasepar('Nbrsec')
        self.Sbase = float(PSLF.GetCasepar('Sbase'))

        ## Agent Collections
        self.Area = []
        self.Bus = []
        self.Gens = []
        self.Load = []
        self.Slack = []
        self.Perturbance = []
        self.Dynamics = []

        # initialize mirror = 
        ltd.mirror.create_mirror_agents(self)
        ltd.mirror.findGlobalSlack(self)

        # Combined Collections
        self.Machines = self.Slack + self.Gens

        # TODO: As logging capability added to agents, add to Log collection
        self.Log = [self] + self.Load + self.Bus + self.Machines

        # Check mirror accuracy in each Area, create machines list for each area
        for c_area in range(self.Narea):
            if self.debug: print("*** Verifying area data...")
            valid = self.Area[c_area].checkArea()
            if valid != 0:
                print("Mirror inaccurate in Area %d, error code: %d" % (c_area, valid))

        # init_dynamics
        self.PSLFmach = []
        self.PSLFgov = []
        self.PSLFexc = []
        
        # read dyd, create pslf models
        # TODO: handle dyd replacement of previous models...
        ltd.data.parseDyd(self, locations['dydPath'])
        
        # link H and mbase to mirror
        ltd.mirror.initInertiaH(self)

        # Handle user input system inertia
        # NOTE: H is typically MW*sec unless noted as PU or in PSLF models
        if self.Hinput > 0.0:
            self.Hsys = self.Hinput
        else:
            self.Hsys = self.ss_H

        print("*** Python Mirror intialized.")

    # Simulation Methods
    def runSim(self):
        if not self.debug:
            # block pslf output for normal (non-debug) runs
            noPrintStr = "dispar[0].noprint = 1"
            PSLF.RunEpcl(noPrintStr)

        """Function to run LTD simulation"""
        print("\n*** Starting Simulation")
        # set flag for non-convergence
        sysCrash = 0

        # Initalization value of Pe for [c_dp-1] functionality
        # NOTE: python does negative indexing, 
        # These values are appeneded now and popped once simulation ends
        ltd.mirror.initRunningVals(self)
        self.r_ss_Pe.append(ltd.mirror.sumPe(self))
        self.r_ss_Pacc.append(0.0)
        self.r_f.append(1.0)
        self.r_fdot.append(0.0)

        # Step Initialize Dynamic Agents
        for x in range(len(self.Dynamics)):
                self.Dynamics[x].stepInitDynamics()

        # Start Simulation loop
        while self.c_t <= self.endTime:
            if self.debug:
                print("\n*** Data Point %d" % self.c_dp)
                print("*** Simulation time: %.2f" % (self.c_t))
            else:
                print("Simulation Time: %7.2f   " % self.c_t), # to print dots each step

            # Step System Wide dynamics
            ltd.mirror.combinedSwing(self, self.ss_Pacc)
            if self.c_f <= 0.0:
                # check for silly frequency
                N = self.c_dp - 1
                sysCrash = 1
                break;

            # Step Individual Agent Dynamics
            for x in range(len(self.Dynamics)):
                self.Dynamics[x].stepDynamics()

            # set pe = pm (dynamic action)
            for x in range(len(self.Machines)):
                self.Machines[x].Pe = self.Machines[x].Pm
            
            # Initialize Pertrubance delta
            self.ss_Pert_Pdelta = 0.0 # required for Pacc calculation
            self.ss_Pert_Qdelta = 0.0 # intended for system loss calculations

            # Step Perturbance Agents
            for x in range(len(self.Perturbance)):
                self.Perturbance[x].step()

            # Sum system loads to Account for any load changes from Perturbances
            self.ss_Pload, self.ss_Qload = ltd.mirror.sumLoad(self)

            # Sum current system Pm 
            self.ss_Pm = ltd.mirror.sumPm(self)
            
            # Calculate current system Pacc
            self.ss_Pacc = (
                self.ss_Pm 
                - self.r_ss_Pe[self.c_dp-1] # Most recent PSLF sum
                - self.ss_Pert_Pdelta
                )
            
            # Find current system Pacc Delta
            # NOTE: unused variable as of 2/2/19
            self.r_Pacc_delta[self.c_dp] = self.ss_Pacc - self.r_ss_Pacc[self.c_dp-1]

            # Distribute Pacc to system machines Pe and solve PSLF
            try:
                ltd.mirror.distPe(self, self.ss_Pacc )
            # Check for convergence
            except ValueError as e:
                # Catches error thown for non-convergene
                print("*** Error Caught, Simulation Stopping...")
                print(e)
                # Pop void data from agents that log
                N = self.c_dp
                sysCrash = 1
                break;

            # update system Pe after PSLF power flow solution
            self.ss_Pe = ltd.mirror.sumPe(self)

            # step log of Agents with ability
            for x in range(len(self.Log)):
                self.Log[x].logStep()

            # step time and data point
            self.r_t[self.c_dp] = self.c_t
            self.c_dp += 1
            self.c_t += self.timeStep

        print("_______________________")
        print("    Simulation Complete\n")

        # remove initialization values
        if sysCrash == 1:
            for x in range(len(self.Log)):
                    self.Log[x].popUnsetData(N)
        else:
            self.r_ss_Pe.pop(len(self.r_ss_Pe) -1)
            self.r_ss_Pacc.pop(len(self.r_ss_Pacc) -1)
            self.r_f.pop(len(self.r_f) -1)
            self.r_fdot.pop(len(self.r_fdot)-1)

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
                'notes' : self.notes,
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
        tag2 = "Created from:\t%s\n" %(self.locations['savPath'])
        created = str(self.created)
        tag3 = "Created on:\t\t%s" %(created)

        return(tag1+tag2+tag3)
