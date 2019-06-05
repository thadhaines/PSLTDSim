class BranchAgent(object):
    """Branch Agent class for LTD"""
    def __init__(self, mirror, area, newBranch):
        # mirror Reference
        self.mirror = mirror
        self.Area = area

        self.Ck = str(newBranch.Ck) # string
        self.ScanBus = int(newBranch.GetScanBusIndex()) #int <- use this to get PSLF objects

        self.TbusIndex = int(newBranch.Ito)
        self.FbusIndex = int(newBranch.Ifrom)

        # LTD references <- have to initialize after all buses are in LTD.
        self.Tbus = None
        self.Fbus = None

        # Current Values
        self.cv= {
            'St': int(newBranch.St),
            }

        #debug
        #print('branch %d id %s from bus %d' % 
        #(self.ScanBus, self.Ck, self.FbusIndex))

        # This may be unneccessary - but could be used for Ymatrix...
        self.X = round(float(newBranch.Zsecx),6) 
        self.R = round(float(newBranch.Zsecr),6)
        self.B = round(float(newBranch.Bsec),6) # seems to round
        self.Length = float(newBranch.Lngsec)

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Fbus.Extnum).zfill(3), self.Fbus.Busnam)
        # additional outputs
        tag3 = "%s %s" %(str(self.Tbus.Extnum).zfill(3), self.Tbus.Busnam)

        return(tag1+' From '+tag2+' to '+tag3)
    

    def createLTDlinks(self):
        """Create links to LTD system"""
        self.Tbus = ltd.find.findBus(self.mirror,
                                     col.BusDAO.FindByIndex(self.TbusIndex).Extnum)
        self.Fbus = ltd.find.findBus(self.mirror,
                                     col.BusDAO.FindByIndex(self.FbusIndex).Extnum)

    def getPref(self):
        """Return reference to PSLF object"""
        return col.BranchDAO.FindByIndex(self.ScanBus)

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
               'AgentType': 'Branch',
               'ScanBus':self.ScanBus,
               'St': self.cv['St'],
               }
        return msg

    def recAMQPmsg(self,msg):
        """Set message values to agent values"""
        self.cv['St'] = msg['St']
        if self.mirror.AMQPdebug: 
            print('AMQP values set!')

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_St = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_St[n] = self.cv['St']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_St = self.r_St[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {
             'St': self.r_St,
             }
        return d