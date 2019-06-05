from .GeneratorAgent import GeneratorAgent

class SlackAgent(GeneratorAgent):
    """Derived from GeneratorAgent for Slack Generator"""
    def __init__(self, mirror, parentBus, newGen):
        super(SlackAgent, self).__init__(mirror, parentBus, newGen)
        self.globalSlack = 0
        #self.areaSlack = 0 # may not be needed

        self.mirror = mirror
        self.Tol = mirror.slackTol

        # Current Values
        self.cv={
            'St' : int(newGen.St),
            'Pe' : ltd.data.single2float(newGen.Pgen),   # Generated Power
            'Pref' : ltd.data.single2float(newGen.Pgen),
            'Q' : ltd.data.single2float(newGen.Qgen),    # Q generatred
            'Pm' : ltd.data.single2float(newGen.Pgen),       # Initialize as equal
            'IRP_flag': 1,      # Inertia response participant flag
            'Pe_calc' : ltd.data.single2float(newGen.Pgen), # for initial ss
            'Pe_error' : 0.0,
            }

        #self.Pe_calc = self.Pe # for initial ss
        #self.Pe_error = 0.0

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Generator',
               'Busnum':self.Busnum,
               'Id': self.Id,
               'Pe': self.cv['Pe'],
               'Pm': self.cv['Pm'],
               'Pref' : self.cv['Pref'],
               'Q': self.cv['Q'],
               'St':self.cv['St'],
               'Pe_calc':self.cv['Pe_calc'],
               'Pe_error': self.cv['Pe_error'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['Pe'] = msg['Pe']
        self.cv['Pm'] = msg['Pm']
        self.cv['Pref'] = msg['Pref']
        self.cv['Q'] = msg['Q']
        self.cv['St'] = msg['St']
        self.cv['Pe_calc'] = msg['Pe_calc']
        self.cv['Pe_error'] = msg['Pe_error']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

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
        self.r_Pe[self.mirror.c_dp] = self.cv['Pe']
        self.r_Pm[self.mirror.c_dp] = self.cv['Pm']
        self.r_Pref[self.mirror.c_dp] = self.cv['Pref']
        self.r_Q[self.mirror.c_dp] = self.cv['Q']
        self.r_St[self.mirror.c_dp] = self.cv['St']
        self.r_Pe_calc[self.mirror.c_dp] = self.cv['Pe_calc']
        self.r_Pe_error[self.mirror.c_dp] = self.cv['Pe_error']

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
             'Mbase' : self.Mbase,
             'Hpu' : self.Hpu,
             'Pe_calc' : self.r_Pe_calc,
             'Pe_error' : self.r_Pe_error,
             'Slack' : 1,
             }
        return d