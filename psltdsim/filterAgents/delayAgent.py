class delayAgent(object):
    """
    An agent that delays input by x samples
    and applies additional filtering if specified
    of the form: outVal = inVal * exp(-$d1)/(1+$t1)
    where d1 is a time delay that is divisible by the timestep 
    (Note: d1 can not be less than the timestep)
    and t1 is the time constant for the lowpass filter
    """

    def __init__(self, parentAgent, mirror, initVal, paramTuple):
        
        self.parentAgent = parentAgent
        self.mirror = mirror
        self.name = self.parentAgent.delayDict['name']
        self.ts = self.mirror.timeStep
        self.d1 = paramTuple[0] # delay time constant
        self.t1 = paramTuple[1] # filter time constant

        self.operate = True
        if len(paramTuple)>=3:
            self.operate = paramTuple[2] # operate bool
        
        
        self.initVal = initVal 

        self.bufferSize = int(self.d1/self.ts)
        self.buffer = [self.initVal]*self.bufferSize
        self.offSet = 0.0

        self.Enable = True
        if self.bufferSize == 0:
            print("*** Delay Error in %s. bufferSize == 0."
                  % self.name)
            self.Enable = False

        if self.t1 != 0.0:
            self.filter = ltd.filterAgents.lowPassAgent( self.mirror, self, self.t1, initVal = self.initVal)
        else:
            self.filter = None
            
    def step(self, inputVal):
        """
        Handle buffer output/input, 
        filtering if required
        """
        if self.Enable and self.operate:
            t = self.mirror.cv['t']

            buffNDX = int(t/self.ts % self.bufferSize)
            outVal = self.buffer[buffNDX- self.offSet] # minus 1 for... Pref tested... Not -1 for w delay... why?

            self.buffer[buffNDX] = inputVal

            if self.filter != None:
                outVal = self.filter.stepFilter(outVal)

            #print(inputVal, outVal) # debug
            return outVal
        else:
            # if delay is not enabled, act as a hold (i.e. ignore input) (act as constant)
            print('*** Delay %s not Enabled...' % self.name)
            outVal = self.buffer[0]
            if self.filter != None:
                outVal = self.filter.stepFilter(outVal)
            # add options to act as through?
            return outVal