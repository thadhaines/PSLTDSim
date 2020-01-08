class BranchAgent(object):
    """Branch Agent class for LTD"""
    def __init__(self, mirror, area, newBranch):
        # mirror Reference
        self.mirror = mirror
        self.Area = area

        self.Ck = str(newBranch.Ck) # string
        self.Id = self.Ck # used in __repr__
        self.ScanBus = int(newBranch.GetScanBusIndex()) #int <- use this to get PSLF objects
        self.Sec = int(newBranch.GetNsec())

        self.FbusIndex = int(newBranch.Ifrom)
        self.TbusIndex = int(newBranch.Ito)

        # LTD references <- have to initialize after all buses are in LTD.
        self.Bus = None # also known as the from bus - simplified to follow other agents info
        self.TBus = None

        self.Islanded = False
        self.ValidBus = False

        # Current Values
        self.cv= {
            'St': int(newBranch.St),
            'Amps' : 0.0,
            'Pbr' : 0.0, # Power flow of Branch
            'Qbr' : 0.0, # Reqctive Power flow of Branch
            }

        # This may be unneccessary - but could be used for Ymatrix...
        self.X = round(float(newBranch.Zsecx),6) # reactance
        self.R = round(float(newBranch.Zsecr),6) # resistance
        self.B = round(float(newBranch.Bsec),6) # susceptance (seems to round)
        self.Length = float(newBranch.Lngsec) #  'informational only'

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
        # added 11/13/19
        if (self.Islanded == False) and self.ValidBus:
            
            Vs = self.Bus.cv['Vm']*self.Bus.Basekv # sending
            ds = self.Bus.cv['Va'] # radians
            Vr = self.TBus.cv['Vm']*self.TBus.Basekv # recieving
            dr = self.TBus.cv['Va'] # radians
            j = 1j

            zBase = self.Bus.Basekv*self.Bus.Basekv/self.mirror.Sbase

            # alt Flow calcs using Amps
            # 1E3 for kV, 1E6 conversion for MW
            try:
                # calculate branch amps, assumes X and R are set in pu and not 0
                Amp = (Vs*1e3*np.exp(j*ds)-Vr*1e3*np.exp(j*dr))/((self.R+j*self.X)*zBase)/np.sqrt(3)
            except ZeroDivisionError:
                Amp = 0.0 

            self.cv['Amps'] = abs(Amp) 

            Pr = Vs*1e3*abs(Amp)*np.cos(ds-np.angle(Amp))*np.sqrt(3)/1E6
            self.cv['Pbr'] = Pr #MW
            
            Qr = Vs*1e3*abs(Amp)*np.sin(ds-np.angle(Amp))*np.sqrt(3)/1E6
            self.cv['Qbr'] = Qr #MW


        else:
            self.cv['Pbr'] = 0.0
            self.cv['Qbr'] = 0.0
            self.cv['Amps'] = 0.0

    def createLTDlinks(self):
        """Create links to LTD system"""
        # run from IPY only
        if self.mirror.debug:
            print("*** Creating branch link from index %d to %d..." %
                  (self.FbusIndex , self.TbusIndex))
        fBus = col.BusDAO.FindByIndex(self.FbusIndex)
        tBus = col.BusDAO.FindByIndex(self.TbusIndex)

        # debug prints
        #print(fBus)
        #print(tBus)

        # check if found bus is valid from PSLF
        validBusType = (type(fBus) != type(None)) and (type(tBus) != type(None))
        self.ValidBus = validBusType

        if validBusType == True:
            # check if busses are created in LTD
            nonIslandFBus = (str(fBus.Extnum) not in self.mirror.ignoredBus)
            nonIslandTBus = (str(tBus.Extnum) not in self.mirror.ignoredBus)

            if all([validBusType, nonIslandFBus,nonIslandTBus, True]):
                self.Bus = ltd.find.findBus(
                    self.mirror, fBus.Extnum)
                self.TBus = ltd.find.findBus(
                    self.mirror, tBus.Extnum)
                if self.mirror.debug:
                    print("*** Created branch link between bus %d to %d." %
                        (self.Bus.Extnum , self.TBus.Extnum))
            else:
                self.Islanded = True
                print("*** Bus error in %d or %d..." %
                  (fBus.Extnum , tBus.Extnum))
        else:
            self.Islanded = True
            print("*** Bus error in %d or %d..." %
                  (self.fBus.Extnum , self.tBus.Extnum))

    def getPref(self):
        """Return reference to PSLF object"""
        busBranch = col.BranchDAO.FindByFromBusToBus(self.FbusIndex, self.TbusIndex)
        for branch in busBranch:
            if branch.Ck == self.Ck:
                return branch

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