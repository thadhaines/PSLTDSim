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

        # Characteristic Data
        self.Mbase = float(newGen.Mbase)
        self.H = 0.0
        self.Hpu = 0.0
        self.Pmax = float(newGen.Pmax)
        self.Qmax = float(newGen.Qmax)

        # Q: Should Vsched = self.Bus.Vsched? seems better utilized in PSLF
        self.Vsched = float(newGen.Vcsched) # This value seems unused in PSLF

        # Current Status
        self.St = int(newGen.St)
        self.IRP_flag = 1       # Inertia response participant flag
        self.Pe = float(newGen.Pgen)   # Generated Power
        self.Pm = self.Pe       # Initialize as equal
        self.Pset = self.Pe
        self.Q = float(newGen.Qgen)    # Q generatred

        # PSLF dynamic models
        self.machine_model = False
        self.gov_model = False
        
    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.GeneratorDAO.FindByBusIndexAndId(self.Scanbus,self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pObj = self.getPref()
        self.Pe = float(pObj.Pgen)
        self.Q = float(pObj.Qgen)
        self.St = int(pObj.St)

    def setPvals(self):
        """Send current mirror values to PSLF"""
        pObj = self.getPref()
        pObj.Pgen = self.Pe
        pObj.St = self.St
        pObj.Save()

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Generator',
               'Busnum':self.Busnum,
               'Id': self.Id,
               'Pe': self.Pe,
               'Pm': self.Pm,
               'Q': self.Q,
               'St':self.St,
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.Pe = msg['Pe']
        self.Pm = msg['Pm']
        self.Q = msg['Q']
        self.St = msg['St']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def recDynamicMsg(self,msg):
        """Update machine dynamics from new dyd model information"""
        # will require resetting machine H and system H tot....
        pass

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Pm = [0.0]*self.mirror.dataPoints
        self.r_Pe = [0.0]*self.mirror.dataPoints
        self.r_Pset = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints
        self.r_St = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        self.r_Pe[self.mirror.c_dp] = self.Pe
        self.r_Pm[self.mirror.c_dp] = self.Pm
        self.r_Pset[self.mirror.c_dp] = self.Pset
        self.r_Q[self.mirror.c_dp] = self.Q
        self.r_St[self.mirror.c_dp] = self.St

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Pe = self.r_Pe[:N]
        self.r_Pm = self.r_Pm[:N]
        self.r_Pset = self.r_Pset[:N]
        self.r_Q  =self.r_Q[:N]
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'Pe': self.r_Pe,
             'Pm': self.r_Pm,
             'Pset': self.r_Pset,
             'Q': self.r_Q,
             'St': self.r_St,
             'Mbase' : self.Mbase,
             'Hpu' : self.Hpu,
             'Slack' : 0,
             }
        return d