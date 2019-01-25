"""LTD Core Agent Definitions
Currently includes: Bus, Generator, Slack, Load, and Area agents.
None of which are fully developed.
Most of which use PSLF library col
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

        # History
        self.r_Vm = [0.0]*self.model.dataPoints
        self.r_Va = [0.0]*self.model.dataPoints

    def __str__(self):
        """Possible useful identification function"""
        tag = "Bus "+self.Busnam+" in Area "+self.Area
        return tag

    def getPref(self):
        """Return reference to PSLF object"""
        return col.BusDAO.FindByIndex(self.Scanbus)

    def getPval(self):
        """Get most recent PSLF values"""
        pObj = self.getPref()
        self.Vm = pObj.Vm
        self.Va = pObj.Va

    def logStep(self):
        """Put current values into log"""
        self.getPval()
        self.r_Vm[self.model.c_dp] = self.Vm
        self.r_Va[self.model.c_dp] = self.Va

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Vm': self.r_Vm,
             'Va': self.r_Va,
             'BusName': self.Busnam,
             'BusNum': self.Extnum,
             }
        return d

class GeneratorAgent(object):
    """Generator Agent for LTD Model"""
    def __init__(self, model, parentBus, newGen):
        # Model/Parent Reference
        self.model = model
        self.Bus = parentBus

        # Identification 
        self.Id = newGen.Id
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.Zone = newGen.Zone
        self.Busnam = newGen.GetBusName()
        self.Busnum = newGen.GetBusNumber()
        self.Scanbus = newGen.GetScanBusIndex()
        self.St = int(newGen.St)
        self.MbaseSAV = float(newGen.Mbase)
        self.MbaseDYD = 0.0
        self.H = 0.0
        self.Hpu = 0.0

        # Current Status
        self.IRP_flag = 1       # Inertia response participant flag
        self.Pm = float(newGen.Pgen)   # Voltage Magnitude
        self.Pe = self.Pm       # Initialize as equal
        self.Q = newGen.Qgen    # Q generatred       
        
        # History 
        self.r_Pm = [0.0]*model.dataPoints
        self.r_Pe = [0.0]*model.dataPoints
        self.r_Q = [0.0]*model.dataPoints
        self.r_St = [0.0]*model.dataPoints

        # Children
        self.machine_model = []
        # TODO: implement proportional governor
        self.gov = []
        self.exc = None

    def getPref(self):
        """Return reference to PSLF object"""
        return col.GeneratorDAO.FindByBusIndexAndId(self.Scanbus,self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pRef = self.getPref()
        self.Pe = float(pRef.Pgen)
        self.Q = float(pRef.Qgen)
        self.St = int(pRef.St)

    def setPvals(self):
        """Send current mirror values to PSLF"""
        pRef = self.getPref()
        pRef.Pgen = self.Pe
        pRef.St = self.St
        pRef.Save()

    def logStep(self):
        """Step to record log history"""
        self.getPvals()
        self.r_Pe[self.model.c_dp] = self.Pe
        self.r_Pm[self.model.c_dp] = self.Pm
        self.r_Q[self.model.c_dp] = self.Q
        self.r_St[self.model.c_dp] = self.St

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Q': self.r_Q,
             'St': self.r_St,
             'Mbase' : self.MbaseDYD,
             'Hpu' : self.Hpu,
             'Slack' : 0,
             }
        return d

class SlackAgent(GeneratorAgent):
    """Derived from GeneratorAgent for Slack Generator"""
    def __init__(self, model, parentBus, newGen):
        super(SlackAgent, self).__init__(model, parentBus, newGen)
        self.globalSlack = 0
        #self.areaSlack = 0 # may not be needed

        self.Tol = model.slackTol
        self.Pe_calc = 0.0
        self.Pe_error = 0.0

        self.r_Pe_calc = [0.0]*model.dataPoints
        self.r_Pe_error = [0.0]*model.dataPoints

    def logStep(self):
        """Step to record log history"""
        self.getPvals()
        self.r_Pe[self.model.c_dp] = self.Pe
        self.r_Pm[self.model.c_dp] = self.Pm
        self.r_Q[self.model.c_dp] = self.Q
        self.r_St[self.model.c_dp] = self.St
        self.r_Pe_calc[self.model.c_dp] = self.Pe_calc
        self.r_Pe_error[self.model.c_dp] = self.Pe_error

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Q': self.r_Q,
             'St': self.r_St,
             'Mbase' : self.MbaseDYD,
             'Hpu' : self.Hpu,
             'Pe_calc' : self.r_Pe_calc,
             'Pe_error' : self.r_Pe_error,
             'Slack' : 1,
             }
        return d
       
class LoadAgent(object):
    """Load Agent for LTD Model"""
    def __init__(self,model, parentBus, newLoad):
        # Model/Parent Reference
        self.model = model
        self.Bus = parentBus

        # Identification
        self.Id = newLoad.Id
        self.Area = newLoad.Area
        self.Zone = newLoad.Zone

        # Current Status
        self.P = float(newLoad.P)
        self.Q = float(newLoad.Q)
        self.St = int(newLoad.St)

        # History 
        self.r_P = [0.0]*model.dataPoints
        self.r_Q = [0.0]*model.dataPoints
        self.r_St = [0.0]*model.dataPoints

        # dynamics?

    def getPref(self):
        """Return reference to PSLF object"""
        return col.LoadDAO.FindByBusIndexAndId(self.Bus.Scanbus, self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pRef = self.getPref()
        self.P = float(pRef.P)
        self.Q = float(pRef.Q)
        self.St = int(pRef.St)

    def logStep(self):
        """Step to record log history"""
        self.r_P[self.model.c_dp] = self.P
        self.r_Q[self.model.c_dp] = self.Q
        self.r_St[self.model.c_dp] = self.St

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'P': self.r_P,
             'Q': self.r_Q,
             'St': self.r_St,
             }
        return d

class AreaAgent(object):
    """Area Agent for LTD Model Collections"""
    #NOTE: Account for zones in the future?

    def __init__(self, model, areaNum):
        #from __main__ import col
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
        self.Bus = []
        # if this is how shunts/SVDs work...
        self.Shunt = []
        self.SVD = []

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'AreaNum': self.Area,
             'Ngen': self.Ngen,
             'Nload': self.Nload,
             }
        return d

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