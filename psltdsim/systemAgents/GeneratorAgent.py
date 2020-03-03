class GeneratorAgent(object):
    """Generator Agent for LTD mirror"""
    def __init__(self, mirror, areaAgent, parentBus, newGen):
        # mirror/Parent Reference
        self.mirror = mirror
        self.Bus = parentBus

        # Identification 
        self.Id = str(newGen.Id)
        self.Lid = newGen.Lid
        self.Area = newGen.Area
        self.AreaAgent = areaAgent
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
        self.Mbase = float(newGen.Mbase) #* removed singled to float function
        self.H = 0.0
        self.Hpu = 0.0
        self.Pmax = float(newGen.Pmax)#*
        self.Qmax0 = float(newGen.Qmax)#*
        self.Qmin0 = float(newGen.Qmin)#*
        self.TurbineType = newGen.TurbineType

        # Q: Should Vsched = self.Bus.Vsched? seems better utilized in PSLF
        self.Vsched = float(newGen.Vcsched) #* This value seems unused in PSLF

        # Current Status
        self.cv={
            'IRPflag': True,      # Inertia response participant flag...
            'P0' : float(newGen.Pgen),
            'Pe' : float(newGen.Pgen),   # Generated Power
            'Pm' : float(newGen.Pgen),   # Initialize as equal
            'Pref' : float(newGen.Pgen), # Steady state init
            'Pref0' : float(newGen.Pgen), # Steady state init
            'Mbase' : self.Mbase, #
            'Q' : float(newGen.Qgen),    # Q generatred
            'Qmin' : self.Qmin0,
            'Qmax' : self.Qmax0,
            'SCE' : 0.0, # station control error - never really implemented.
            'St' : int(newGen.St),
            'R' : 666E6, # workaround until gov.cv dict....
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
        
        self.cv['Pe'] = float(pObj.Pgen)
        self.cv['Q'] = float(pObj.Qgen)
        self.cv['Qmax'] = float(pObj.Qmax)
        self.cv['Qmin'] = float(pObj.Qmin)

        # TODO: Handle State changes that occur in PSLF? (i.e. WECC auto trips)
        self.cv['St'] = int(pObj.St)


    def setPvals(self):
        """Send current mirror values to PSLF"""
        pObj = self.getPref()
        # DEBUG update of voltage magnitude
        #if self.mirror.debug:
        #    print("* %d %s \tPe changed from \t %.5f \t to %.5f" %
        #    (self.Busnum, self.Busnam, pObj.Pgen, self.cv['Pe']*self.cv['St']))

        pObj.Pgen = self.cv['Pe']
        pObj.Qmax = self.cv['Qmax']
        pObj.Qmin = self.cv['Qmin']
        pObj.St = self.cv['St']

        """ Obsolete Code
        # State changes handled in step agent (03/02/20)
        if pObj.St != self.cv['St']:
            # a change in status has occured
            pObj.St = self.cv['St']
            if self.cv['St'] == 0:
                #pObj.SetOutOfService()
                #if self.mirror.debug: print('setting out of service....')
                pObj.Pgen = 0.0
                pObj.Qmax = 0.0
                pObj.Qmin = 0.0
            elif self.cv['St'] == 1:
                #pObj.SetInService()
                # return Q limits to original setting
                pObj.Qmax = self.Qmax0
                pObj.Qmin = self.Qmin0
        """

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
               'Qmin': self.cv['Qmin'],
               'Qmax': self.cv['Qmax'],
               'St':self.cv['St'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['Pe'] = msg['Pe']
        self.cv['Pm'] = msg['Pm']
        self.cv['Pref'] = msg['Pref']
        self.cv['Q'] = msg['Q']
        self.cv['Qmin'] = msg['Qmin']
        self.cv['Qmax'] = msg['Qmax']
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