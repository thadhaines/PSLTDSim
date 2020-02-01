class ShuntAgent(object):
    """Shunt Agent for LTD mirror"""
    #NOTE : incomplete as of 5/16/19. only basic id and casting functionality.
    def __init__(self,mirror,parentBus,newShunt):

        # mirror Reference
        self.mirror = mirror
        self.Bus = parentBus
        
        # Identification 
        self.Area = int(newShunt.Area)
        self.Zone = int(newShunt.Zone)
        self.Id = str(newShunt.Id)
        
        # Properties
        self.B = float(newShunt.B) # PU Capacitance # was single2float....
        self.G = float(newShunt.G) # PU Inductance # was single2float....
        
        # From Bus information
        self.FBusnam = str(newShunt.GetBusName())
        self.FBusnum = int(newShunt.GetBusNumber())
        self.Fkv = float(newShunt.GetBusBasekv()) # was single2float....

        # To Bus Information
        self.TBusnam = str(newShunt.GetToBusName())
        self.TBusnum = int(newShunt.GetToBusNumber())
        self.Tkv = float(newShunt.GetToBusBasekv())#ltd.data.single2float(newShunt.GetToBusBasekv())

        # Current Status
        self.cv={
            'St' : int(newShunt.St),
            }

        # Children
        self.Timer ={}

        self.existsInPSLF = self.getPref()

        if self.existsInPSLF != None:
            self.existsInPSLF = 1
        else:
            self.existsInPSLF = 0


    def __repr__(self):
        #Display more useful data for mirror
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s %s" %(str(self.FBusnum).zfill(3), self.Id, self.FBusnam)

        return(tag1+tag2)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.ShuntDAO.FindBusShunt(self.Bus.Scanbus, self.Id)

    def getPvals(self):
        """Make current status reflect PSLF values"""
        pObj = self.getPref()
        self.cv['St'] = int(pObj.St)

    def setPvals(self):
        """Set PSLF values"""
        pObj = self.getPref()
        pObj.St = int(self.cv['St'])
        pObj.Save()

    def makeAMQPmsg(self):
        """Make AMQP message to send cross process"""
        msg = {'msgType' : 'AgentUpdate',
               'AgentType': 'Shunt',
               'Busnum':self.Bus.Extnum,
               'Id': self.Id,
               'St': int(self.cv['St']),
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['St'] = int(msg['St'])
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_St = [0.0]*self.mirror.dataPoints
        self.r_Q = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_St[n] = self.cv['St']
        # Running Q is positive for Capacitive MVARS
        self.r_Q[n] = (self.B*self.mirror.Sbase - self.G*self.mirror.Sbase)*self.cv['St']
        
    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_St = self.r_St[:N]
        self.r_Q = self.r_Q[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {
             'St': self.r_St,
             'Q' : self.r_Q,
             }
        return d