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

        # Case Parameters
        self.Nload = len(col.LoadDAO.FindByBus(self.Scanbus))
        self.Ngen = len(col.GeneratorDAO.FindByBus(self.Scanbus))

        # Children
        self.Gens = []
        self.Slack = []
        self.Load = []

        # if this is how shunts/SVDs work...
        self.Shunt = []
        self.SVD = []

        # Current Status
        self.Vm = newBus.Vm     # Voltage Magnitude
        self.Va = newBus.Va     # Voltage Angle (radians)

    def __str__(self):
        """Possible useful identification function"""
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def getPval(self):
        """Get most recent PSLF values"""
        pObj = col.BusDAO.FindByIndex(self.Scanbus)
        self.Vm = pObj.Vm
        self.Va = pObj.Va

class GeneratorAgent(object):
    """Generator Agent for LTD Model"""
    def __init__(self, model, parentBus, newGen):
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
        self.St = newGen.St
        self.MbaseSAV = newGen.Mbase
        self.MbaseDYD = 0.0
        self.H = 0.0
        self.Hpu = 0.0

        # Current Status
        self.IRP_flag = 1       # Inertia response participant flag
        self.Pm = newGen.Pgen   # Voltage Magnitude
        self.Pe = self.Pm       # Initialize as equal
        self.Q = newGen.Qgen    # Q generatred

        # NOTE: the idea is to have current status variables for easy access,
        # then move them to a time sequence list at each step
        # could use current time as an index (would allow for pre-allocation)

        # Parent
        self.Bus = parentBus

        # Children
        self.machine_model = []
        # could be an empty list for each type
        self.gov = None
        # TODO : add functionality to check and record history

class SlackAgent(GeneratorAgent):
    """Derived from GeneratorAgent for Slack Generator"""
    def __init__(self, model, parentBus, newGen):
        super(SlackAgent, self).__init__(model, parentBus, newGen)
        # attempt at deriving SlackAgent from Generator Agent
        # mostly a placehold class for inheritance confirmation
        self.Tol = model.slackTol
        self.Pe_calc = [0.0]
        self.Pe_error = [0.0]

        # TODO : add functionality to check and record history

class LoadAgent(object):
    """Load Agent for LTD Model"""
    def __init__(self,model, parentBus, newLoad):
        # Model Reference
        self.model = model
        self.Bus = parentBus

        # Identification
        self.Id = newLoad.Id
        self.Area = newLoad.Area
        self.Zone = newLoad.Zone

        # Current Status
        self.P = newLoad.P   
        self.Q = newLoad.Q 
        self.St = newLoad.St

        # TODO : add functionality record history - changes handled by perturbances
        # dynamics?

    def getPref(self):
        """Return reference to PSLF object"""
        return col.LoadDAO.FindByBusIndexAndId(self.Bus.Scanbus, self.Id)

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
        self.Machines = []
        # if this is how shunts/SVDs work...
        self.Shunt = []
        self.SVD = []

    def checkArea(self):
        """Checks if found number of Generators and loads is Correct
        Creates Machine list
        Returns 0 if all valid, -1 for invalid Generators, -2 for invalid loads
        """
        # Q: check for SVD & shunts?
        self.Machines = self.Slack + self.Gens

        if self.Ngen == (len(self.Machines)):
            if self.model.debug: 
                print("Gens correct in Area:\t%d" % self.Area)
            
        else:
            print("*** Gen Error: %d/%d found. Area:\t%d" % 
                  (len(self.Machines), self.Ngen, self.Area))
            return -1

        if self.Nload == len(self.Load):
            if self.model.debug: 
                print("Load correct in Area:\t%d" % self.Area)
        else:
            print("*** Load Error: %d/%d found. Area:\t%d" % 
                  (len(self.Load), self.Nload, self.Area))
            return -2

        return 0