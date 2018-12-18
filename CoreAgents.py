"""LTD Core Agent Definitions
Currently includes: Bus, Generator, Slack, Load, and Area agents.
None of which are fully developed.
"""

class BusAgent(object):
    """Bus Agent for LTD Model"""
    def __init__(self, model, newBus):
        # Model Reference
        self.model = model

        # Identification 
        self.Area = newBus.Area
        self.Busnam = newBus.Busnam
        self.Extnum = newBus.Extnum
        self.Scanbus = newBus.GetScanBusIndex()
        self.Type = newBus.Type

        # Current Status
        self.Vm = newBus.Vm     # Voltage Magnitude
        self.Va = newBus.Va     # Voltage Angle (radians)
        
        # Case Parameters
        self.Nload = len(col.LoadDAO.FindByBus(self.Scanbus))
        self.Ngen = len(col.GeneratorDAO.FindByBus(self.Scanbus))

        # Children
        self.Gens = []
        self.Slack = []
        self.Load = []

    def __str__(self):
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def getPval(self):
        """Get most recent PSLF values"""
        pObj = col.BusDAO.FindByIndex(self.Scanbus)
        self.Vm = pObj.Vm
        self.Va = pObj.Va

class GeneratorAgent(object):
    """Generator Agent for LTD Model"""
    def __init__(self, model, newGen):
        # Model Reference
        self.model = model

        # Identification 
        self.Id = newGen.Id
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.Zone = newGen.Zone
        self.Busnam = newGen.GetBusName()
        self.Busnum = newGen.GetBusNumber()
        self.Scanbus = newGen.GetScanBusIndex()
        self.Mbase = newGen.Mbase
        self.St = newGen.St
        self.H = 0.0

        # Current Status
        self.Pm = newGen.Pgen   # Voltage Magnitude
        self.Pe = self.Pm       # Initialize as equal
        self.Q = newGen.Qgen    # Q generatred

        # NOTE: the idea is to have current status variables for easy access,
        # then move them to a time sequence list at each step
        # could use current time as an index (would allow for pre-allocation)

        # Children
        self.dynamics = []

class SlackAgent(GeneratorAgent):
    """Derived from GeneratorAgent for Slack Generator"""
    def __init__(self, model, newGen):
        super(SlackAgent, self).__init__(model, newGen)
        # attempt at deriving SlackAgent from Generator Agent
        # mostly a placehold class for inheritance confirmation
        self.Tol = 0.01 # UNDONE: will be set in model params....
        self.Pe_calc = 0.0
        self.Pe_error = 0.0

class LoadAgent(object):
    """Load Agent for LTD Model"""
    def __init__(self,model, newLoad):
        # Model Reference
        self.model = model

        # Identification
        self.Id = newLoad.Id
        self.Area = newLoad.Area
        self.Zone = newLoad.Zone

        # Current Status
        self.P = newLoad.P   
        self.Q = newLoad.Q 
        self.St = newLoad.St

class AreaAgent(object):
    """Area Agent for LTD Model Collections"""
    def __init__(self, model, areaNum):
        # Model Reference
        self.model = model

        # Identification
        self.Area = areaNum

        # Case Parameters
        self.Ngen = len(col.GeneratorDAO.FindByArea(self.Area))
        self.Nload = len(col.LoadDAO.FindByArea(self.Area))

        # Children
        self.Gens = []
        self.Load = []
        self.Slack = []

    def checkArea(self):
        """Checks if found number of Generators and loads is Correct"""
        if self.Ngen == (len(self.Gens)+len(self.Slack)):
            if self.model.debug: 
                print("Gens correct in Area:\t%d" % self.Area)
            
        else:
            print("*** Gen Error: %d/%d found. Area:\t%d" % 
                  ((len(self.Gens)+len(self.Slack)), self.Ngen, self.Area))

        if self.Nload == len(self.Load):
            if self.model.debug: 
                print("Load correct in Area:\t%d" % self.Area)
        else:
            print("*** Load Error: %d/%d found. Area:\t%d" % 
                  (len(self.Load), self.Nload, self.Area))