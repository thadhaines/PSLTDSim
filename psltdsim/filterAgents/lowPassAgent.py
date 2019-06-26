class lowPassAgent():
    """Class to low pass filter input and track input and state"""

    def __init__(self, mirror, parentAgent, T1, initVal = 0.0):
        self.mirror = mirror
        self.parentAgent = parentAgent # mirror agent that uses this filter
        self.T1 = T1

        self.initVal = initVal

        self.inVal = initVal
        self.outVal = initVal

        self.t = [0 , self.mirror.timeStep] # will have to be moved if ts = variable
        self.appenedData = True

        # Dynamic init
        self.sys1 = sig.StateSpace([-1.0/self.T1],[1.0/self.T1],[1.0],0.0)

        # attach self to mirror and mirror Log list
        self.mirror.Filter.append(self)
        self.mirror.Log.append(self)

        if mirror.debug:
            print("*** Low Pass Filter added to %s" % (self.parentAgent))

    def stepFilter(self, inputSignal):
        """ Perform governor control"""
        self.inVal = inputSignal # get newest set value.

        # Create system input
        uVector = np.array([self.inVal,self.inVal])

        # First (and only) dynamic Block
        _, y1, self.x1 = sig.lsim(self.sys1, U=uVector, T=self.t, 
                                   X0=self.r_x1[self.mirror.cv['dp']-1], interp=True)

        self.mirror.DynamicSolns += 1

        # Set and return outVal
        self.outVal = float(y1[1]) # float because y1 is numpy array
        return self.outVal

    def initRunningVals(self):
        """Initialize History Values of dynamic agent"""
        # History Values
        self.r_inVal = [0.0]*self.mirror.dataPoints
        self.r_x1 = [0.0]*self.mirror.dataPoints

        # Append init values to running state data
        self.r_x1.append(self.initVal)

    def logStep(self):
        """Update Log information"""
        self.r_inVal[self.mirror.cv['dp']] = self.inVal
        self.r_x1[self.mirror.cv['dp']] = float(self.x1[1])

    def popUnsetData(self, N):
        """Remove any appened init values from running values"""
        self.r_inVal = self.r_inVal[:N]
        self.r_x1 = self.r_x1[:N]
