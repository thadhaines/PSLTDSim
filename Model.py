"""Model for agent based LTD simulations"""

from __main__ import *

# load .NET dll
import clr              
clr.AddReferenceToFileAndPath(locations[0])
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col

class Model(object):
    """Model class for LTD Model"""
    def __init__(self, locations, Htot = 0, debug = 0):
        """Carries out initialization 
        This includes: PSLF, python mirror, dynamics, and perturbances
        """
        # Simulation Parameters
        self.locations = locations
        self.debug = debug

        # init pslf and solve system
        self.pslf = self.init_PSLF()
        self.LTD_Solve()

        # init_mirror
        ## Case Parameters
        self.Ngen = self.pslf.GetCasepar('Ngen')
        self.Nbus = self.pslf.GetCasepar('Nbus')
        self.Nload = self.pslf.GetCasepar('Nload')
        self.Narea = self.pslf.GetCasepar('Narea')
        self.Nzone = self.pslf.GetCasepar('Nzone')
        # Q: branch sections = lines?
        self.Nbrsec = self.pslf.GetCasepar('Nbrsec') 

        ## Agent Collections
        self.Area = []
        self.Bus = []
        self.Gens = []
        self.Load = []
        self.Slack = []

        self.init_mirror()

        # init_dynamics

        # Systemwide Variables (after init_dynamics so that H can be summed)
        self.Htot = Htot # TODO: check later to decide if manual input dectected
        self.f = 1
        self.t = 0 

        # NOTE: Variable names may change after a varibale naming convention has been decided
        # ss_ .. system sum
        self.ss_Pe = 0.0
        self.ss_Pm = 0.0
        self.ss_Qgen = 0.0
        self.ss_Qload = 0.0
        self.ss_Pload = 0.0
        self.PLosses = 0.0
        self.QLosses = 0.0
        self.ss_Pacc = 0.0
        
        # init perturbances. Maybe just an addPertutbance method.?

    # Initiazliaze Methods
    def init_PSLF(self):
        """Initialize instance of PSLF with given paths. 
        Returns pslf object, prints error code, or crashes.
        """
        # create pslf instance / object
        pslf = mid.Pslf(self.locations[1])   
        # load .sav file
        load_test = pslf.LoadCase(self.locations[2])     

        if load_test == 0:
            print(self.locations[2] + " Successfully loaded.")
            return pslf
        else:
            print("Failure to load .sav")
            print("Error code: %d" % test)
            return None

    def init_mirror(self):
        """Create python mirror of PSLF system
        Handles Buses, Generators, and Loads
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
                    newGenAgent = SlackAgent(m_ref, b_gen[c_gen])
                    # add references to gen in model and bus,area agent
                    newBusAgent.Slack.append(newGenAgent)
                    self.Slack.append(newGenAgent)
                    areaAgent.Slack.append(newGenAgent)
                else:
                    newGenAgent = GeneratorAgent(m_ref, b_gen[c_gen])
                    # add references to gen in model and bus,area agent
                    newBusAgent.Gens.append(newGenAgent)
                    self.Gens.append(newGenAgent)
                    areaAgent.Gens.append(newGenAgent)

        # locate and create bus load children
        if newBusAgent.Nload > 0:
            b_load = col.LoadDAO.FindByBus(newBusAgent.Scanbus)
            for c_load in range(newBusAgent.Nload):
                newLoadAgent = LoadAgent(m_ref, b_load[c_load])
                # add references to load in model and bus,area agent
                newBusAgent.Load.append(newLoadAgent)
                self.Load.append(newLoadAgent)
                areaAgent.Load.append(newLoadAgent)

        self.Bus.append(newBusAgent)

    # Simulation Methods
    def LTD_Solve(self):
        """Function to use custom solve parameters
        Local file manipulation requierd to perform without PSLF errors.
        """
        return self.pslf.SolveCase(
            25, # maxIterations, 
	        0, 	# iterationsBeforeVarLimits, 
	        0,	# flatStart, 
	        1,	# tapAdjustment, 
	        1,	# switchedShuntAdjustment, 
	        1,	# phaseShifterAdjustment, 
	        1,	# gcdAdjustment, ?
	        0,	# areaInterchangeAdjustment, <- only setting NOT default?
	        1,	# solnType, 1 == full, 2 == DC, 3 == decoupled 
	        0, # reorder
            )

    def sumPower(self):
        """Function to sum all Pe, Pm, P, and Q of system"""
        for ndx in range(len(self.Gens)):
            #Sum all generator values if status = 1
            if self.Gens[ndx].St == 1:
                self.ss_Pe += self.Gens[ndx].Pe
                self.ss_Pm += self.Gens[ndx].Pm
                self.ss_Qgen += self.Gens[ndx].Q

        for ndx in range(len(self.Slack)):
            #Sum all Slack values if status = 1
            if self.Slack[ndx].St == 1:
                self.ss_Pe += self.Slack[ndx].Pe
                self.ss_Pm += self.Slack[ndx].Pm
                self.ss_Qgen += self.Slack[ndx].Q

        for ndx in range(len(self.Load)):
            #Sum all loads with status == 1
            if self.Load[ndx].St == 1:
                self.ss_Qload += self.Load[ndx].Q
                self.ss_Pload += self.Load[ndx].P

        self.PLosses = self.ss_Pe - self.ss_Pload
        self.QLosses = self.ss_Qgen - self.ss_Qload
        self.ss_Pacc = self.ss_Pm - self.ss_Pe

    # Information Display
    def dispCP(self):
        """Display current Case Parameters"""
        print("*** Case Parameters ***")
        print(".sav ==\t%s" % self.locations[2])
        print("%d Areas" % self.Narea)
        print("%d Zones" % self.Nzone)
        print("%d Busses" % self.Nbus)
        print("%d Generators" % self.Ngen)
        print("%d Loads" % self.Nload)
        print("***_________________***")

    def dispPow(self):
        """Display System Sumation power values"""
        print("*** System Power Overview ***")
        print("Pm:\t%.2f" % self.ss_Pm)
        print("Pe:\t%.2f" % self.ss_Pe)
        print("Pacc:\t%.2f" % self.ss_Pacc)
        print("Pload:\t%.2f" % self.ss_Pload)
        print("Ploss:\t%.2f" % self.PLosses)
        print("Qgen:\t%.2f" % self.ss_Qgen)
        print("Qload:\t%.2f" % self.ss_Qload)
        print("Qloss:\t%.2f" % self.QLosses)
        print("***_______________________***")