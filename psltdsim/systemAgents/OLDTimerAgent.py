class OLDTimerAgent(object):
    """Debug timer
    A timer that accumulates time if given condition is met then
     raises an activation flag if enough time has been accumulated."""

    def __init__(self, mirror, name, timerStr):
        # Retain Inputs / mirror reference
        self.name = name
        self.timerStr = timerStr
        self.mirror = mirror

        parsed = timerStr.split(":")
        if len(parsed) < 4:
            print('*** Timer Error: Underdefined input.')
            foundAgent = False
        else:
            # Parse and cast input
            self.idStr = parsed[0].split()
            self.attr = parsed[1].strip() # Value in target agent cv dictionary
            self.cond = parsed[2].strip() # a string ex: <.95
            self.actTime = float(parsed[3].strip())
            # Attempt to find mirror Agent
            foundAgent = ltd.find.findAgent(self.mirror ,self.idStr[0], self.idStr[1:] )

        if foundAgent:
            if self.mirror.debugTimer:
                print('Found', foundAgent)
            self.agentRef = foundAgent
            if self.attr not in foundAgent.cv:
                print('*** Timer Error: Agent has no attribute %s.' % self.attr)
                self.attrRef = False
            else:
                self.attrRef = True
        else:
            print('*** Timer Error: Target Agent Not Found.')
            self.agentRef = None

        # Accumulators
        self.currentAcc = 0.0
        self.totalAcc = 0.0
        self.totalAct = 0
        self.totalReset = 0

        # Current Values
        self.cv = {
            'Acc' : 0,
            'Act' : 0,
            }

        # Flags
        self.actFlag = False

        # Attach timer to refereneced agent and mirror
        if self.agentRef:
            self.agentRef.Timer[self.name] = self
            if (self.idStr[0].lower() != 'mirror'):
                self.mirror.Timer[self.name] = self
            self.mirror.Log.append(self)
            print('*** Added %s ' % self)

    def step(self):
        """Check conditional, handle accumulation logic, raise flag if required"""
        if self.agentRef and self.attrRef:
            if self.mirror.debugTimer:
                print('Stepping '+self.name)

            # Check timer condition
            if eval(str(self.agentRef.cv[self.attr])+self.cond):
                if self.mirror.debugTimer:
                    print(str(self.agentRef.cv[self.attr])+' ' +self.cond,' is True')
                # accumulate time
                self.currentAcc += self.mirror.timeStep
                self.totalAcc += self.mirror.timeStep
                self.cv['Acc'] = 1
            else:
                if self.mirror.debugTimer:
                    print(str(self.agentRef.cv[self.attr])+' ' +self.cond,' is False')
                # reset timer
                self.currentAcc = 0.0
                self.cv['Acc'] = 0

            if (self.currentAcc >= self.actTime) and not self.actFlag:
                # only raise flag if not raised
                self.actFlag = True
                self.totalAct +=1
                self.cv['Act'] = 1
        else:
            # Avoid crash if no agentRef
            pass

    def reset(self):
        """ Reset current accumulation time and reset activation flag"""
        self.currentAcc = 0.0
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
        tag2 = "Activated when:  %s %s %s for %d seconds" %(self.idStr ,self.attr, self.cond, self.actTime)

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