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
            'Pm' : ltd.data.single2float(newGen.Pgen),   # Initialize as equal
            'Pref' : ltd.data.single2float(newGen.Pgen), # Steady state init
            'P0' : ltd.data.single2float(newGen.Pgen),
            'Q' : ltd.data.single2float(newGen.Qgen),    # Q generatred
            'IRP_flag': 1,      # Inertia response participant flag (not used)...
            'Pe_calc' : ltd.data.single2float(newGen.Pgen), # for initial ss
            'Pe_error' : 0.0,
            'SCE' : 0,
            }

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
        self.r_SCE = [0.0]*self.mirror.dataPoints

        self.r_Pe_calc = [0.0]*self.mirror.dataPoints
        self.r_Pe_error = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_Pe[n] = self.cv['Pe']
        self.r_Pm[n] = self.cv['Pm']
        self.r_Pref[n] = self.cv['Pref']
        self.r_Q[n] = self.cv['Q']
        self.r_St[n] = self.cv['St']
        self.r_SCE[n] = self.cv['SCE']
        self.r_Pe_calc[n] = self.cv['Pe_calc']
        self.r_Pe_error[n] = self.cv['Pe_error']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_Pref = self.r_Pref[:N]
        self.r_Q = self.r_Q[:N]
        self.r_St = self.r_St[:N]
        self.r_SCE = self.r_SCE[:N]
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
             'SCE' : self.r_SCE,
             }
        return d