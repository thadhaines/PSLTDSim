from .GeneratorAgent import GeneratorAgent

class SlackAgent(GeneratorAgent):
    """Derived from GeneratorAgent for Slack Generator"""
    def __init__(self, mirror, parentBus, newGen):
        super(SlackAgent, self).__init__(mirror, parentBus, newGen)
        self.globalSlack = 0
        #self.areaSlack = 0 # may not be needed

        self.mirror = mirror
        self.Tol = mirror.slackTol
        self.Pe_calc = 0.0
        self.Pe_error = 0.0

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Pm = [0.0]*self.mirror.dataPoints
        self.r_Pe = [0.0]*self.mirror.dataPoints
        self.r_Pref = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints
        self.r_St = [0.0]*self.mirror.dataPoints

        self.r_Pe_calc = [0.0]*self.mirror.dataPoints
        self.r_Pe_error = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        self.r_Pe[self.mirror.c_dp] = self.Pe
        self.r_Pm[self.mirror.c_dp] = self.Pm
        self.r_Pref[self.mirror.c_dp] = self.Pref
        self.r_Q[self.mirror.c_dp] = self.Q
        self.r_St[self.mirror.c_dp] = self.St
        self.r_Pe_calc[self.mirror.c_dp] = self.Pe_calc
        self.r_Pe_error[self.mirror.c_dp] = self.Pe_error

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_Pref = self.r_Pref[:N]
        self.r_Q = self.r_Q[:N]
        self.r_St = self.r_St[:N]
        self.r_Pe_calc = self.r_Pe_calc[:N]
        self.r_Pe_error = self.r_Pe_error[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Pref': self.r_Pref,
             'Q': self.r_Q,
             'St': self.r_St,
             'Mbase' : self.MbaseDYD,
             'Hpu' : self.Hpu,
             'Pe_calc' : self.r_Pe_calc,
             'Pe_error' : self.r_Pe_error,
             'Slack' : 1,
             }
        return d