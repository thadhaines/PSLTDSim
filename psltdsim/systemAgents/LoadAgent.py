class LoadAgent(object):
    """Load Agent for LTD mirror"""
    def __init__(self,mirror, parentBus, newLoad):
        # mirror/Parent Reference
        self.mirror = mirror
        self.Bus = parentBus
        self.Busnum = parentBus.Extnum

        # Identification
        self.Id = newLoad.Id
        self.Area = newLoad.Area
        self.Zone = newLoad.Zone

        # Current Status
        self.cv = {
            'P' : ltd.data.single2float(newLoad.P),
            'Q' : ltd.data.single2float(newLoad.Q),
            'St' : int(newLoad.St),
            }
        #self.P = ltd.data.single2float(newLoad.P)
        #self.Q = ltd.data.single2float(newLoad.Q)
        #self.St = int(newLoad.St)
        # dynamics?

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Bus.Extnum).zfill(3), self.Bus.Busnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.LoadDAO.FindByBusIndexAndId(self.Bus.Scanbus, self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pObj = self.getPref()
        self.cv['P'] = ltd.data.single2float(pObj.P)
        self.cv['Q'] = ltd.data.single2float(pObj.Q)
        self.cv['St'] = int(pObj.St)

    def setPvals(self):
        """Set PSLF values"""
        pObj = self.getPref()
        pObj.P = self.cv['P']
        pObj.Q = self.cv['Q']
        pObj.St = self.cv['St']
        pObj.Save()

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Load',
               'Busnum':self.Busnum,
               'Id': self.Id,
               'P': self.cv['P'],
               'Q': self.cv['Q'],
               'St': self.cv['St'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['P'] = msg['P']
        self.cv['Q'] = msg['Q']
        self.cv['St'] = msg['St']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_P = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints
        self.r_St = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_P[n] = self.cv['P']
        self.r_Q[n] = self.cv['Q']
        self.r_St[n] = self.cv['St']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_P = self.r_P[:N]
        self.r_Q = self.r_Q[:N]
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'P': self.r_P,
             'Q': self.r_Q,
             'St': self.r_St,
             }
        return d