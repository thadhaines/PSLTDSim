"""Test of seperated files"""
"""visual studio often requires deleting default ironpython environment, and using 2.7 (no bit declaration)"""

from __main__ import *

import clr              # required to load .NET dll
clr.AddReferenceToFileAndPath(locations[0])
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col

# Model Creation
class Model(object):
    """Model class for LTD Model"""
    def __init__(self, locations, Htot = 0):
        """Carries out initialization of PSLF, python mirror, dynamics, and perturbances"""
        self.locations = locations

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
        self.Gen = []
        self.Load = []
        self.Slack = []

        self.init_mirror()

        # init_dynamics

        # Systemwide Variables
        self.Htot = Htot # will be checked later to decide if manual input dectected
        self.f = 1
        self.ct = 0 # current time
        
        # init pert

    # Initiazliaze Methods
    def init_PSLF(self):
        """Attempts to initialize instance of PSLF with given paths. Returns pslf object"""
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
        """Create mirror of PSLF system"""
        c_area = 0
        f_bus = 0
        f_gen = 0
        f_load = 0

        while f_bus < self.Nbus:
            #while not all busses are found
            a_busses = col.AreaDAO.FindBusesInArea(c_area)
            n_bus = len(a_busses)
            if n_bus > 0:
                #If Current area has buses
                self.Area.append(c_area)
                f_bus += n_bus
        
                for c_bus in range(n_bus):
                    #for each found bus
                    self.Bus.append(Bus(a_busses[c_bus]))
                    b_gen = col.GeneratorDAO.FindByBus(a_busses[c_bus].Extnum)
                    n_gen = len(b_gen)
                    b_load = col.LoadDAO.FindByBus(a_busses[c_bus].Extnum)
                    n_load = len(b_load)
                    f_gen += n_gen
                    f_load += n_load
                    print("%s \thas %d gen and %d load" % (a_busses[c_bus].Busnam, n_gen, n_load))

            c_area +=1
            
        print("Found %d buses" % f_bus)
        print("Found %d gens" % f_gen)
        print("Found %d loads" % f_load)

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
    def caseParams(self):
        """Fucntion displays current Case Parameters"""
        print(".sav ==\t%s" % self.locations[2])
        print("%d Areas \t%d Zones" % (self.Narea, self.Nzone))
        print("%d Busses\t%d Generators\t%d Loads" % (self.Nbus, self.Ngen, self.Nload))