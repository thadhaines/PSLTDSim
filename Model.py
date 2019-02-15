"""Model for agent based LTD simulations"""

"""
    NOTE: Should probably be refactored 
"""

from __main__ import *

class Model(object):
    """Model class for LTD Model"""
    def __init__(self, locations, simParams, debug = 0):
        """Carries out initialization 
        This includes: PSLF, python mirror, and dynamics
        """
        global PSLF
        from datetime import datetime

        __module__= "Model"
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
        
        # initial system solve
        try:
            self.LTD_Solve()
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
        self.init_mirror()
        self.findGlobalSlack()

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
        parseDyd(self, locations['dydPath'])
        
        # link H and mbase to mirror
        self.init_H()

        # Handle user input system inertia
        # NOTE: H is typically MW*sec unless noted as PU or in PSLF models
        if self.Hinput > 0.0:
            self.Hsys = self.Hinput
        else:
            self.Hsys = self.ss_H

        print("*** Python Mirror intialized.")

    # Initiazliaze Methods
    def init_mirror(self):
        """Create python mirror of PSLF system by 'crawling' area busses
        Handles Buses, Generators, and Loads
        Uses col
        TODO: Add agents for every object: shunts, SVD, xfmr, branch sections, ...
        """
        # Useful variable notation key:
        # c_ .. current
        # f_ .. found
        # a_ .. area
        # n_ .. number of

        c_area = 0
        f_bus = 0
        f_gen = 0
        f_load = 0

        if self.debug: 
            print("*** Crawling system for agents...")
            print("Extnum\tgen\tload\tBusnam")

        while f_bus < self.Nbus:
            #while not all busses are found
            a_busses = col.AreaDAO.FindBusesInArea(c_area)
            n_bus = len(a_busses)
            if n_bus > 0:
                #If Current area has buses
                newAreaAgent = AreaAgent(self, c_area)
                f_bus += n_bus

                for c_bus in range(n_bus):
                    #for each found bus
                    self.incorporateBus(a_busses[c_bus], newAreaAgent)
                    c_ScanBus = a_busses[c_bus].GetScanBusIndex()
                    n_gen = len(col.GeneratorDAO.FindByBus(c_ScanBus))
                    n_load = len(col.LoadDAO.FindByBus(c_ScanBus))
                    f_gen += n_gen
                    f_load += n_load

                    if self.debug: 
                        print("%d\t%d\t%d\t%s" % 
                                         (a_busses[c_bus].Extnum, 
                                          n_gen, 
                                          n_load,
                                          a_busses[c_bus].Busnam)
                                         )
                self.Area.append(newAreaAgent)
            c_area += 1
        
        if self.debug:
            print("Found %d Areas" % len(self.Area))
            print("Found %d buses" % f_bus)
            print("Found %d gens (%d Slack)" % (f_gen, len(self.Slack)))
            print("Found %d loads" % f_load)

    # Additional init Methods
    def incorporateBus(self, newBus, areaAgent):
        """Handles adding Busses and associated children to Mirror"""
        # b_ .. Bus objects
        # c_ .. Current Object
        # m_ .. model
        m_ref = areaAgent.model # to simplify referencing
        slackFlag = 0
        if newBus.Type == 0:
            slackFlag = 1

        newBusAgent = BusAgent(m_ref, newBus)

        # locate and create bus generator children
        if (newBusAgent.Ngen > 0):
            b_gen = col.GeneratorDAO.FindByBus(newBusAgent.Scanbus)
            for c_gen in range(newBusAgent.Ngen):

                if slackFlag:
                    newGenAgent = SlackAgent(m_ref, newBusAgent, b_gen[c_gen])
                    # add references to gen in model and bus,area agent
                    newBusAgent.Slack.append(newGenAgent)
                    self.Slack.append(newGenAgent)
                    areaAgent.Slack.append(newGenAgent)
                else:
                    newGenAgent = GeneratorAgent(m_ref, newBusAgent, b_gen[c_gen])
                    # add references to gen in model and bus,area agent
                    newBusAgent.Gens.append(newGenAgent)
                    self.Gens.append(newGenAgent)
                    areaAgent.Gens.append(newGenAgent)

        # locate and create bus load children
        if newBusAgent.Nload > 0:
            b_load = col.LoadDAO.FindByBus(newBusAgent.Scanbus)
            for c_load in range(newBusAgent.Nload):
                newLoadAgent = LoadAgent(m_ref, newBusAgent, b_load[c_load])
                # add references to load in model and bus,area agent
                newBusAgent.Load.append(newLoadAgent)
                self.Load.append(newLoadAgent)
                areaAgent.Load.append(newLoadAgent)

        self.Bus.append(newBusAgent)
        areaAgent.Bus.append(newBusAgent)

    def init_H(self):
        """Link H and Mbase from PSLF dyd dynamic models to mirror machines
        Will calculate ss_H
        """
        # pdmod = pSLF dYNAMIC modLE
        if self.debug: print("*** Linking PSLF H to python environment...")
        linkedModels = 0

        for pdmod in range(len(self.PSLFmach)): # for each found pslf model
            mirrorGen = findGenOnBus(self, self.PSLFmach[pdmod].Busnum)

            if mirrorGen:
                mirrorGen.Hpu = self.PSLFmach[pdmod].H
                mirrorGen.MbaseDYD = self.PSLFmach[pdmod].Mbase
                # NOTE: PSLF .sav Mbase and .dyd Mbase may be different
                # dyd values overwrite any sav values (Via PSLF user manual)
                mirrorGen.H = self.PSLFmach[pdmod].H *self.PSLFmach[pdmod].Mbase
                self.ss_H += mirrorGen.H 
                # add refernece to PSLF machine model in python mirror
                mirrorGen.machine_model.append(self.PSLFmach[pdmod])
                if self.debug: print("PSLF model linked to %s" % mirrorGen)
                linkedModels +=1

        if self.debug: print("*** Linked %d/%d PSLF models to system." % (linkedModels,len(self.PSLFmach)))

    def findGlobalSlack(self):
        """Locates and sets the global slack generator"""
        #NOTE: Not even close to complete
        if len(self.Slack) < 2:
            self.Slack[0].globalSlack = 1
        else:
            print("More than 1 slack generator found... Setting first to global... ")
            self.Slack[0].globalSlack = 1

    # Simulation Methods
    def runSim(self):
        """Function to run LTD simulation"""
        print("\n*** Starting Simulation")
        # set flag for non-convergence
        sysCrash = 0

        # Initalization value of Pe for [c_dp-1] functionality
        # NOTE: python does negative indexing, 
        # These values are appeneded now and popped once simulation ends
        self.r_ss_Pe.append(self.sumPe())
        self.r_ss_Pacc.append(0.0)
        self.r_f.append(1.0)
        self.r_fdot.append(0.0)

        # Step Initialize Dynamic Agents
        for x in range(len(self.Dynamics)):
                self.Dynamics[x].stepInitDynamics()        

        # Start Simulation loop
        while self.c_t <= self.endTime:
            print("\n*** Data Point %d" % self.c_dp)
            print("*** Simulation time: %.2f" % (self.c_t))

            # Step System Wide dynamics
            combinedSwing(self, self.ss_Pacc)
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
            self.ss_Pload, self.ss_Qload = self.sumLoad()

            # Sum current system Pm 
            self.ss_Pm = self.sumPm()
            
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
                distPe(self, self.ss_Pacc )
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
            self.ss_Pe = self.sumPe()

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

    def LTD_Solve(self):
        """Solves power flow using custom solve parameters
        Returns PSLF errorCode if available
        Only option not default is area interchange adjustment (turned off)
        """
        global PSLF
        """
        # open 2 fds
        null_fds = [os.open(os.devnull, os.O_RDWR) for x in xrange(2)]
        # save the current file descriptors to a tuple
        save = os.dup(1), os.dup(2)
        # put /dev/null fds on 1 and 2
        os.dup2(null_fds[0], 1)
        os.dup2(null_fds[1], 2)
        """
        errorCode = PSLF.SolveCase(
            25, # maxIterations, Solpar.Itnrmx
	        0, 	# iterationsBeforeVarLimits, Solpar.Itnrvl
	        0,	# flatStart, 
	        1,	# tapAdjustment, Solpar.Tapadj
	        1,	# switchedShuntAdjustment, Solpar.Swsadj
	        1,	# phaseShifterAdjustment, Solpar.Psadj
	        0,	# gcdAdjustment, probably Solpar.GcdFlag
	        0,	# areaInterchangeAdjustment, 
	        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
	        0,  # reorder (in dypar default = 0)
            )

        # restore file descriptors so I can print the results
        os.dup2(save[0], 1)
        os.dup2(save[1], 2)
        # close the temporary fds
        os.close(null_fds[0])
        os.close(null_fds[1])

        if self.debug: print('Power Flow Solution returns: %d' % errorCode)

        if errorCode == -1:
            '''Solution did not converge'''
            raise ValueError('PSLF power flow solution did not converge.')
            return


    def addPert(self, tarType, idList, perType, perParams):
        """Add Perturbance to model.
        tarType = 'Load'
        idList = [Busnumber, id] id is optional, first object chosen by default
        perType = 'Step'
        perParams = list of specific perturbance parameters, will vary
            for a step: perParams = [targetAttr, tStart, newVal]
        NOTE: could be refactored to a seperate file
        TODO: Add other tarTypes ('Gen') and perTypes ('Ramp')
        """

        #Locate target in mirror
        if tarType == 'Load':
            if len(idList) < 2:
                targetObj = findLoadOnBus(self, idList[0])
            else:
                targetObj = findLoadOnBus(self, idList[0], idList[1])

        #Create Perturbance Agent
        if (perType == 'Step') and targetObj:
            # perParams = [targetAttr, tStart, newVal, type='r']
            newStepAgent = LoadStepAgent(self, targetObj, perParams)
            self.Perturbance.append(newStepAgent)
            print("*** Perturbance Agent added!")
            print(newStepAgent)
            return

        print("*** Perturbance Agent error - nothing added.")


    def sumPm(self):
        """Returns sum of all mechanical power from active machines"""
        sysPm = 0.0
        for ndx in range(len(self.Machines)):
            #Sum all generator values if status = 1
            if self.Machines[ndx].St == 1:               
                sysPm += self.Machines[ndx].Pm

        return sysPm

    def sumPe(self):
        """Returns sum of all electrical power from active machines
        Uses most recent PSLF values (update included in function)
        """
        sysPe = 0.0
        for ndx in range(len(self.Machines)):
            #Sum all generator values if status = 1
            if self.Machines[ndx].St == 1:
                self.Machines[ndx].getPvals()
                sysPe += self.Machines[ndx].Pe

        return sysPe

    def sumLoad(self):
        """Returns system sums of active PSLF load as [Pload, Qload]"""
        Pload = 0.0
        Qload = 0.0
        for ndx in range(len(self.Load)):
            self.Load[ndx].getPvals()
            #Sum all loads with status == 1
            if self.Load[ndx].St == 1:
                Pload += self.Load[ndx].P
                Qload += self.Load[ndx].Q

        return [Pload,Qload]

    def sumPower(self):
        """Not used - for reference on calculating losses only - to be removed
        
        Function to sum all Pe, Pm, P, and Q of system
        NOTE: Only matches real power until SVD and Shunts are modeled
        TODO: split apart for more concise usage during simulation
        """
        # reset system sums
        self.ss_Pe = 0.0
        self.ss_Pm = 0.0
        self.ss_Qgen = 0.0
        self.ss_Qload = 0.0
        self.ss_Pload = 0.0

        for ndx in range(len(self.Machines)):
            #Sum all generator values if status = 1
            if self.Machines[ndx].St == 1:
                self.Machines[ndx].getPvals()
                self.ss_Pe += self.Machines[ndx].Pe
                self.ss_Pm += self.Machines[ndx].Pm
                self.ss_Qgen += self.Machines[ndx].Q

        for ndx in range(len(self.Load)):
            #Sum all loads with status == 1
            if self.Load[ndx].St == 1:
                self.Load[ndx].getPvals()
                self.ss_Qload += self.Load[ndx].Q
                self.ss_Pload += self.Load[ndx].P

        # NOTE: Commented out perturbance delta due to where sumPower() is placed,
        # if placed before case is solved, these are required to correctly
        # account for losses
        self.PLosses = self.ss_Pe - self.ss_Pload #+ self.ss_Pert_Pdelta
        self.QLosses = self.ss_Qgen - self.ss_Qload #+ self.ss_Pert_Qdelta

        self.ss_Pacc = self.ss_Pm - self.ss_Pe

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
