class DTCTimerAgent(object):
    """
    For Use from DTC Agent
    A timer that accumulates time if given condition is met then
    raises an activation flag if enough time has been accumulated.
    """

    def __init__(self, mirror, DTCAgent, name, timerD):
        # Retain Inputs & mirror reference
        self.name = name
        self.mirror = mirror
        self.DTCAgent = DTCAgent
        self.timerD = timerD
        self.actTime = timerD['actTime']
        self.logic = timerD["logic"]

        ###
        # Accumulators
        self.AccWindowSize = int(self.actTime / self.mirror.timeStep)
        self.windowNDX = -1
        self.currentAcc = [0.0]*self.AccWindowSize
        self.totalAcc = 0.0
        self.totalAct = 0
        self.totalReset = 0

        # Current Values
        self.cv = {
            'Acc' : 0, # current time step accumulation status
            'Act' : 0, # Running value for action Flag
            }

        # Flags
        self.actFlag = False

        # Attach timer to refereneced agent and mirror
        self.DTCAgent.Timer[self.name] = self
        self.mirror.Timer[self.name] = self
        self.mirror.Log.append(self)
        print('*** Added %s ' % self)

    def step(self):
        """Check conditional, handle accumulation logic, raise flag if required"""
        if self.mirror.debugTimer:
            print('Stepping '+self.name)

        #t = self.mirror.cv['dp']
        self.windowNDX +=1
        self.windowNDX %= self.AccWindowSize

        # Get referenes use exec.
        # creates temporary vaiables named the same as the ra
        # required for logic string to be evaluated
        for ra in self.DTCAgent.ra:
            exec(ra+'='+str(self.DTCAgent.ra[ra].getNewAttr()))

        # Check timer condition
        if eval(self.logic):
            if self.mirror.debugTimer:
                print(self.logic+' is True')
            # accumulate time step
            self.currentAcc[self.windowNDX] = self.mirror.timeStep
            self.totalAcc += self.mirror.timeStep
            self.cv['Acc'] = 1 
        else:
            if self.mirror.debugTimer:
                print(self.logic+' is False')
            # reset timer
            self.currentAcc[self.windowNDX] = 0.0
            self.cv['Acc'] = 0

        if (sum(self.currentAcc) >= self.actTime) and not self.actFlag:
            # only raise flag if not raised
            self.actFlag = True
            self.totalAct +=1
            self.cv['Act'] = 1

    def reset(self):
        """ Reset current accumulation time and reset activation flag"""
        self.currentAcc = [0.0]*self.AccWindowSize
        self.totalReset +=1
        self.cv['Act'] = 0
        self.actFlag = False

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  " <%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Activated when:  %s is True for %d seconds" %(
            self.logic, self.actTime)

        return(self.name+tag1+tag2)

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_Acc = [0.0]*self.mirror.dataPoints
        self.r_Act = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Put current values into log"""
        n = self.mirror.cv['dp']
        self.r_Acc[n] = self.cv['Acc']
        self.r_Act[n] = self.cv['Act']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_Acc = self.r_Acc[:N]
        self.r_Act = self.r_Act[:N]