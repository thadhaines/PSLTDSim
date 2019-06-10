class BusAgent(object):
    """Bus Agent for LTD mirror"""
    def __init__(self, mirror, newBus):

        # mirror Reference
        self.mirror = mirror

        # Identification 
        self.Area = newBus.Area
        self.Busnam = newBus.Busnam
        self.Extnum = newBus.Extnum
        self.Scanbus = newBus.GetScanBusIndex()
        self.Type = newBus.Type

        # Case Parameters
        self.Nload = len(col.LoadDAO.FindByBus(self.Scanbus))
        self.Ngen = len(col.GeneratorDAO.FindByBus(self.Scanbus))
        self.Nshunt = len(col.ShuntDAO.FindAnyShuntsByBus(self.Scanbus))

        # Children (objects attached to bus)
        self.Gens = []
        self.Slack = []
        self.Load = []
        self.Shunt = []
        self.SVD = []

        # Current Status
        self.cv = {
            'Vm' :newBus.Vm,
            'Va' : newBus.Va,
            }
        #self.Vm = newBus.Vm     # Voltage Magnitude
        #self.Va = newBus.Va     # Voltage Angle (radians)
        

        # Voltage settings
        #self.Vmax = newBus.Vmax # These values don't seem to be always set
        #self.Vmin = newBus.Vmin
        self.Basekv = ltd.data.single2float(newBus.Basekv)
        self.Vsched = ltd.data.single2float(newBus.Vsched)



    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Extnum).zfill(3), self.Busnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.BusDAO.FindByIndex(self.Scanbus)

    def getPvals(self):
        """Get most recent PSLF values"""
        pObj = self.getPref()
        self.cv['Vm'] = pObj.Vm
        self.cv['Va'] = pObj.Va

        #self.Vm = pObj.Vm
        #self.Va = pObj.Va

    def setPvals(self):
        """Set PSLF values"""
        pObj = self.getPref()
        pObj.Vm = self.Vsched
        pObj.Save()

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Bus',
               'Extnum':self.Extnum,
               'Vm': self.cv['Vm'],
               'Va': self.cv['Va'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['Vm'] = msg['Vm']
        self.cv['Va'] = msg['Va']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Vm = [0.0]*self.mirror.dataPoints
        self.r_Va = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Put current values into log"""
        n = self.mirror.cv['dp']
        self.r_Vm[n] = self.cv['Vm']
        self.r_Va[n] = self.cv['Va']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Vm = self.r_Vm[:N]
        self.r_Va = self.r_Va[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        # Used to compare data in MATLAB
        d = {'Vm': self.r_Vm,
             'Va': self.r_Va,
             'BusName': self.Busnam,
             'BusNum': self.Extnum,
             }
        return d