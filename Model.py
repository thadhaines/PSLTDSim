"""Test of seperated files"""
"""VS may require default ironpython environment (no bit declaration)"""

from __main__ import *

import clr              # required to load .NET dll
clr.AddReferenceToFileAndPath(locations[0])
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col

# Model Creation
class Model(object):
    """Model class for LTD Model"""
    def __init__(self, locations, Htot = 0, debug = 0):
        """Carries out initialization 
        This includes: PSLF, python mirror, dynamics, and perturbances
        """
        self.locations = locations
        self.debug = debug

        ## init pslf
        self.pslf = self.init_PSLF()
        self.LTD_Solve()

        ## init_mirror
        ### Case Parameters
        self.Ngen = self.pslf.GetCasepar('Ngen')
        self.Nbus = self.pslf.GetCasepar('Nbus')
        self.Nload = self.pslf.GetCasepar('Nload')
        self.Nbrsec = self.pslf.GetCasepar('Nbrsec') # branch sections = lines?
        self.Narea = self.pslf.GetCasepar('Narea')
        self.Nzone = self.pslf.GetCasepar('Nzone')

        # Agent Collections
        self.Area = []
        self.Bus = []
        self.Gens = []
        self.Load = []
        self.Slack = []

        self.init_mirror()

        # init_dynamics

        # Systemwide Variables
        self.Htot = Htot # will be checked later to decide if manual input dectected
        self.f = 1
        self.ct = 0 # current time
        
        # init perturbances...

    # Initiazliaze Methods
    def init_PSLF(self):
        """Initialize instance of PSLF with given paths. 
        Returns pslf object, prints error code, or crashes.
        """
        pslf = mid.Pslf(self.locations[1])   # create pslf instance / object
        load_test = pslf.LoadCase(self.locations[2])     # load .sav file

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
        c_area = 0
        f_bus = 0
        f_gen = 0
        f_load = 0

        if self.debug: print("Extnum\tgen\tload\tBusnam")

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

                    if self.debug: print("%d\t%d\t%d\t%s" % 
                                         (a_busses[c_bus].Extnum, 
                                          n_gen, 
                                          n_load,
                                          a_busses[c_bus].Busnam,)
                                         )
                self.Area.append(newAreaAgent)
            c_area +=1
        
        if self.debug:
            print("Found %d Areas" % len(self.Area))
            print("Found %d buses" % f_bus)
            print("Found %d gens" % f_gen)
            print("Found %d loads" % f_load)

    # Additional init Methods
    def incorporateBus(self,newBus,areaAgent):
        """Handles adding Busses and associated children to Mirror"""
        # b_... Bus objects
        # c_... Current Object
        newBusAgent = BusAgent(areaAgent.model, newBus)

        if newBusAgent.Ngen > 0:
            b_gen = col.GeneratorDAO.FindByBus(newBusAgent.Scanbus)
            for c_gen in range(newBusAgent.Ngen):
                newGenAgent = GeneratorAgent(areaAgent.model, b_gen[c_gen])
                # add references to gen in model and bus,area agent
                newBusAgent.Gens.append(newGenAgent)
                self.Gens.append(newGenAgent)
                areaAgent.Gens.append(newGenAgent)

        if newBusAgent.Nload > 0:
            b_load = col.LoadDAO.FindByBus(newBusAgent.Scanbus)
            for c_load in range(newBusAgent.Nload):
                newLoadAgent = LoadAgent(areaAgent.model, b_load[c_load])
                # add references to load in model and bus,area agent
                newBusAgent.Load.append(newLoadAgent)
                self.Load.append(newLoadAgent)
                areaAgent.Load.append(newLoadAgent)

        self.Bus.append(newBusAgent)

    # Simulation Methods
    def LTD_Solve(self):
        """Function to use custom solve parameters"""
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