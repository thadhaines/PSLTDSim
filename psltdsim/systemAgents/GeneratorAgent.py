class GeneratorAgent(object):
    """Generator Agent for LTD mirror"""
    def __init__(self, mirror, parentBus, newGen):
        # mirror/Parent Reference
        self.mirror = mirror
        self.Bus = parentBus

        # Identification 
        self.Id = newGen.Id
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.Zone = newGen.Zone
        self.Busnam = newGen.GetBusName()
        self.Busnum = newGen.GetBusNumber()
        self.Scanbus = newGen.GetScanBusIndex()
        self.globalSlack = False
        self.areaSlack = False

        # Used for BA distribution 
        self.distType = None 
        self.ACEpFactor = None

        # Characteristic Data
        self.Mbase = ltd.data.single2float(newGen.Mbase)
        self.H = 0.0
        self.Hpu = 0.0
        self.Pmax = ltd.data.single2float(newGen.Pmax)
        self.Qmax = ltd.data.single2float(newGen.Qmax)

        # Q: Should Vsched = self.Bus.Vsched? seems better utilized in PSLF
        self.Vsched = ltd.data.single2float(newGen.Vcsched) # This value seems unused in PSLF

        # Current Status
        self.cv={
            'IRPflag': False,      # Inertia response participant flag...
            'P0' : ltd.data.single2float(newGen.Pgen),
            'Pe' : ltd.data.single2float(newGen.Pgen),   # Generated Power
            'Pm' : ltd.data.single2float(newGen.Pgen),   # Initialize as equal
            'Pref' : ltd.data.single2float(newGen.Pgen), # Steady state init
            'Q' : ltd.data.single2float(newGen.Qgen),    # Q generatred
            'SCE' : 0.0,
            'St' : int(newGen.St),
            }

        # PSLF dynamic models
        self.machine_model = False
        self.gov_model = False

        # Children
        self.Timer = {}
        
    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s '%s'" %( self.Busnam, str(self.Busnum), self.Id)

        return(tag1+tag2)

    def calcSCE(self):
        """ Calculate Station Control Error (if < 0, more power required) """
        self.cv['SCE'] = self.cv['Pe'] - self.cv['P0']

    def getPref(self):
        """Return reference to PSLF object"""
        return col.GeneratorDAO.FindByBusIndexAndId(self.Scanbus,self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pObj = self.getPref()
        
        self.cv['Pe'] = ltd.data.single2float(pObj.Pgen)
        self.cv['Q'] = ltd.data.single2float(pObj.Qgen)
        self.cv['St'] = int(pObj.St)

    def setPvals(self):
        """Send current mirror values to PSLF"""
        pObj = self.getPref()
        pObj.Pgen = self.cv['Pe']*self.cv['St']

        if pObj.St != self.cv['St']:
            # a change in status has occured
            if self.cv['St'] == 0:
                pObj.SetOutOfService()
                if self.mirror.debug: print('setting out of service....')
                pObj.Pgen = 0.0
            elif self.cv['St'] == 1:
                pObj.SetInService()
            pObj.St = self.cv['St']
        pObj.Save()

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
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['Pe'] = msg['Pe']
        self.cv['Pm'] = msg['Pm']
        self.cv['Pref'] = msg['Pref']
        self.cv['Q'] = msg['Q']
        self.cv['St'] = msg['St']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Pe = [0.0]*self.mirror.dataPoints
        self.r_Pm = [0.0]*self.mirror.dataPoints
        self.r_Pref = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints
        self.r_SCE = [0.0]*self.mirror.dataPoints
        self.r_St = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_Pe[n] = self.cv['Pe'] * float(self.cv['St'])
        self.r_Pm[n] = self.cv['Pm'] * float(self.cv['St'])
        self.r_Pref[n] = self.cv['Pref']
        self.r_Q[n] = self.cv['Q'] * float(self.cv['St'])
        self.r_SCE[n] = self.cv['SCE']
        self.r_St[n] = self.cv['St']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_Pref = self.r_Pref[:N]
        self.r_Q  =self.r_Q[:N]
        self.r_SCE = self.r_SCE[:N]
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Pref': self.r_Pref,
             'Q': self.r_Q,
             'St': self.r_St,
             'SCE' : self.r_SCE,
             'Mbase' : self.Mbase,
             'Hpu' : self.Hpu,
             'Slack' : 0,
             }
        return d