class TimerAgent(object):
    """
    For Use from shunt control Agent (assumes RefAgent is known)
    A timer that accumulates time if given condition is met then
    raises an activation flag if enough time has been accumulated.
    Allows for percent type of activation via running 'Window' Accumulation
    """

    def __init__(self, mirror, name, RefAgent, logicSTR, actTime, countType='abs'):
        # Retain Inputs & mirror reference
        self.name = name
        self.mirror = mirror
        self.RefAgent = RefAgent

        self.actTime = actTime # seconds

        # Handle optional 'percent' check
        self.countType = countType
        if len(self.countType.strip().split(' ')) > 1:
            self.percent = float(self.countType.strip().split(' ')[1])
        else:
            self.percent = 1.0

        # Parse Timer Logic
        self.logicSTR = logicSTR
        parsed = logicSTR.split(":")
        self.attr = parsed[0].strip() # Value in target agent cv dictionary
        self.cond = parsed[1].strip() # a string ex: <.95

        if self.attr not in self.RefAgent.cv:
            print('*** Timer Error: Agent has no attribute %s.' % self.attr)
            self.attrRef = False
        else:
            self.attrRef = True

        # Accumulators
        self.AccWindowSize = int(self.actTime / self.mirror.timeStep)
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
        if self.RefAgent:
            self.RefAgent.Timer[self.name] = self
            self.mirror.Timer[self.name] = self
            self.mirror.Log.append(self)
            print('*** Added %s ' % self)

    def step(self):
        """Check conditional, handle accumulation logic, raise flag if required"""
        if self.RefAgent and self.attrRef:
            if self.mirror.debugTimer:
                print('Stepping '+self.name)

            t = self.mirror.cv['dp']
            windowNDX = t % self.actTime

            # Check timer condition
            if eval(str(self.RefAgent.cv[self.attr])+self.cond):
                if self.mirror.debugTimer:
                    print(str(self.RefAgent.cv[self.attr])+' ' +self.cond,' is True')
                # accumulate time step
                self.currentAcc[windowNDX] = self.mirror.timeStep
                self.totalAcc += self.mirror.timeStep
                self.cv['Acc'] = 1 
            else:
                if self.mirror.debugTimer:
                    print(str(self.RefAgent.cv[self.attr])+' ' +self.cond,' is False')
                # reset timer
                self.currentAcc[windowNDX] = 0.0
                self.cv['Acc'] = 0

            if (sum(self.currentAcc) >= self.actTime*self.percent) and not self.actFlag:
                # only raise flag if not raised
                self.actFlag = True
                self.totalAct +=1
                self.cv['Act'] = 1
        else:
            # Avoid crash if no RefAgent
            pass

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
        tag2 = "Activated when:  %s %s %s for %d seconds" %(
            self.RefAgent ,self.attr, self.cond, self.actTime)

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