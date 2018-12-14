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
        self.pslf = self.init_PSLF(self.locations)
        self.LTD_Solve(self.pslf)

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

        # init_dynamics

        # Systemwide Variables
        self.Htot = Htot # will be checked later to decide if manual input dectected
        self.f = 1
        self.ct = 0 # current time
        
        # init pert

    # Initiazliaze Methods
    def init_PSLF(self, locations):
        """Attempts to initialize instance of PSLF with given paths. Returns pslf object"""
        pslf = mid.Pslf(locations[1])   # create pslf instance / object
        load_test = pslf.LoadCase(locations[2])     # load .sav file

        if load_test == 0:
            print(locations[2] + " Successfully loaded.")
            return pslf
        else:
            print("Failure to load .sav")
            print("Error code: %d" % test)
            return None

    # Simulation Methods
    def LTD_Solve(self, pslf_object):
        """Function to use custom solve parameters"""
        return pslf_object.SolveCase(
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