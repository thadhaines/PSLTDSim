class TransformerAgent(object):
    """Transformer Agent class for LTD"""
    def __init__(self, mirror, area, newXFMR):
        # mirror Reference
        self.mirror = mirror
        self.Area = area

        self.Ck = str(newXFMR.Ck) # string
        self.Id = self.Ck # used in __repr__
        self.ScanBus = int(newXFMR._Idx) #int <- use this to get PSLF objects

        # from bus info
        self.busName = str(newXFMR.GetBusName())
        self.busKv = float(newXFMR.GetBusBasekv())
        busNum = int(newXFMR.GetBusNumber())

        Bus = col.BusDAO.FindBusByNumberNameKv(busNum, self.busName, self.busKv)
        self.busNum = int(Bus.Extnum)

        # get external to bus number
        self.TbusName = str(newXFMR.GetToBusName())
        self.TbusKv = float(newXFMR.GetToBusBasekv())
        TbusNum = int(newXFMR.GetToBusNumber())

        TBus = col.BusDAO.FindBusByNumberNameKv(TbusNum, self.TbusName, self.TbusKv)
        self.TbusNum = int(TBus.Extnum)

        # LTD references <- have to initialize after all buses are in LTD.
        self.Bus = None # also known as the from bus - simplified to follow other agents info
        self.TBus = None
        self.LinkOk = False

        # Current Values
        self.cv= {
            'St': int(newXFMR.St),
            'Amps' : 0.0,
            'Pbr' : 0.0, # Power flow of Branch
            'Qbr' : 0.0, # Reqctive Power flow of Branch
            }

        # Properties
        self.X = round(float(newXFMR.Zpsx),6) # reactance
        self.R = round(float(newXFMR.Zpsr),6) # resistance

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__

        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        if self.Bus != None:
            # additional outputs
            tag2 = "%s %s" %(str(self.Bus.Extnum), self.Bus.Busnam)
        else:
            tag2 = "None"

        if self.TBus != None:
            # additional outputs
            tag3 = "%s %s" %(str(self.TBus.Extnum), self.TBus.Busnam)
        else:
            tag3 = "None"

        return(tag1+' From '+tag2+' to '+tag3)
    
    def calcFlow(self):
        """Calculate Power flow in MW and AMP flow from self to TBus"""
        if self.LinkOk:
            
            #reworked from branch calcs....
            Vs = self.Bus.cv['Vm'] # sending
            ds = self.Bus.cv['Va'] # radians
            Vr = self.TBus.cv['Vm'] # recieving
            dr = self.TBus.cv['Va'] # radians
            j = 1j

            iBase = self.mirror.Sbase/self.Bus.Basekv*(1E6/1E3)

            # alt Flow calcs using Amps
            # 1E3 for kV, 1E6 conversion for MW
            try:
                # calculate branch amps, assumes X and R are set in pu and not 0
                Amp = (Vs*np.exp(j*ds)-Vr*np.exp(j*dr)) / ((self.R+j*self.X))/np.sqrt(3)*iBase
            except ZeroDivisionError:
                print("Zero div %s", self)
                Amp = 0.0 

            # ratio at end =(vp/vs) used to correctly scale current
            self.cv['Amps'] = abs(Amp)*(self.Bus.Basekv/self.TBus.Basekv)

            # Constants at end to scale PU values
            Pr = Vs*abs(Amp)*np.cos(ds-np.angle(Amp))*np.sqrt(3)*self.Bus.Basekv*1e3/1E6
            self.cv['Pbr'] = Pr #MW
            
            Qr = Vs*abs(Amp)*np.sin(ds-np.angle(Amp))*np.sqrt(3)*self.Bus.Basekv*1e3/1E6
            self.cv['Qbr'] = Qr #MW


        else:
            self.cv['Pbr'] = 0.0
            self.cv['Qbr'] = 0.0
            self.cv['Amps'] = 0.0

    def createLTDlinks(self):
        """Create links to LTD system"""
        # run in PY3
        if self.mirror.debug:
            print("*** Creating XFMR link between bus %d to %d..." %
                  (self.busNum , self.TbusNum))

        # Temp variables for checking logic
        fromBus = False
        toBus = False

        # attempt to link from bus
        bus = ltd.find.findBus(self.mirror, self.busNum)
        if bus != None:
            self.Bus = bus
            fromBus = True

        # attempt to link to bus
        tbus = ltd.find.findBus(self.mirror, self.TbusNum)
        if tbus != None:
            self.TBus = tbus
            toBus = True

        # check if linking was successful
        if all([fromBus, toBus]):
            self.LinkOk = True

    def getPref(self):
        """Return reference to PSLF object"""
        XFMR = col.TransformerDAO.FindByIndex(self.ScanBus)
        return XFMR

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
               'AgentType': 'XFMR',
               'ScanBus':self.ScanBus,
               'Ck' : self.Ck,
               'St': int(self.cv['St']),
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
        self.r_Amps = [0.0]*self.mirror.dataPoints
        self.r_Pbr = [0.0]*self.mirror.dataPoints
        self.r_Qbr = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        self.calcFlow()
        n = self.mirror.cv['dp']
        self.r_St[n] = self.cv['St']
        self.r_Amps[n] = self.cv['Amps']
        self.r_Pbr[n] = self.cv['Pbr']
        self.r_Qbr[n] = self.cv['Qbr']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_St = self.r_St[:N]
        self.r_Amps = self.r_Amps[:N]
        self.r_Pbr = self.r_Pbr[:N]
        self.r_Qbr = self.r_Qbr[:N]

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {
             'St': self.r_St,
             'Amps': self.r_Amps,
             'Pbr': self.r_Pbr,
             'Qbr': self.r_Qbr,
             'Tbus' : self.TBus.Extnum,
             }
        return d