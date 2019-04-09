""" Dynamic Agent Class created from PSLF machine data"""

class tgov1Agent():
    """Agent to perform governor action"""

    def __init__(self, mirror, PSLFgov):
        """Objects created from intPY3Dynamics"""
        self.mirror = mirror
        self.PSFLgov = PSLFgov
        self.Gen = PSLFgov.Gen

        self.appenedData = True

        self.Busnum = PSLFgov.Busnum
        self.Busnam = PSLFgov.Busnam
        self.baseKv = PSLFgov.Base_kV
        self.Id = PSLFgov.Id
        
        self.mwCap = self.Gen.MbaseDYD # default PSLF behaviour, possibly rethink

        self.R  = PSLFgov.R
        self.T1 = PSLFgov.T1
        self.Vmax = PSLFgov.Vmax
        self.Vmin = PSLFgov.Vmin
        self.T2 = PSLFgov.T2
        self.T3 = PSLFgov.T3
        self.Dt = PSLFgov.Dt

        self.t = [0 , self.mirror.timeStep]
        self.leng = 2 # size of t

        # Dynamic init
        self.sys1 = sig.StateSpace([-1.0/self.T1],[1.0/self.T1],
                                   [1.0],0.0)
        self.sys2 = sig.StateSpace([-1.0/self.T3],[1.0/self.T3],
                                   [1.0-self.T2/self.T3],[self.T2/self.T3])

        self.y1HighLimit = self.Vmax * self.mwCap
        self.y1LowLimit = self.Vmin * self.mwCap

        if mirror.debug:
            print("*** Added tgov1 to gen on bus %d '%s'" 
                  % (self.Busnum,self.Busnam))

    def stepDynamics(self):
        """ Perform steam governor control"""
        
        # Create system inputs
        delta_w = self.mirror.c_deltaF*-1.0

        dwVec = np.array([delta_w, delta_w])

        # Perform sum and first gain block
        uVector = dwVec*self.mirror.Sbase/self.R#*self.mirror.Sbase

        # First dynamic Block
        _, y1, self.x1 = sig.lsim(self.sys1, U=uVector, T=self.t, 
                                   X0=self.r_x1[self.mirror.c_dp-1])

        # Second block
        _, y2, self.x2 = sig.lsim(self.sys2, y1, T=self.t,
                                   X0=self.r_x2[self.mirror.c_dp-1])

        # Set Generator Mechanical Power To limited range
        posNewPm = float(y2[1]) + self.Gen.Pm

        if posNewPm > self.y1HighLimit:
            posNewPm = self.y1HighLimit
        elif posNewPm < self.y1LowLimit:
            posNewPm = self.y1LowLimit 

        # Addition of damping
        #posNewPm = posNewPm 
        self.Gen.Pm = posNewPm - delta_w*self.Dt
    def stepInitDynamics(self):
        """ Once H has been initialized, check if K has to be recalculated"""
        pass
        # Doesn't seem like this check is necessary due to previous settings
        if self.mirror.debug:
            print('*** Checking for updated model information...')

        if self.Gen.MbaseSAV != self.Gen.MbaseDYD:
            self.Mbase = self.Gen.MbaseDYD
            if self.mirror.debug:
                print('... updated model.')
            return

        if self.mirror.debug:
            print('... nothing updated.')

    def initRunningVals(self):
        """Initialize History Values of dynamic agent"""
        # History Values
        self.r_x1 = [0.0]*self.mirror.dataPoints
        self.r_x2 = [0.0]*self.mirror.dataPoints

        # Append intit values to running state data
        self.r_x1.append(0.0)
        self.r_x2.append(0.0)

    def logStep(self):
        """Update Log information"""
        self.r_x1[self.mirror.c_dp] = float(self.x1[1])
        self.r_x2[self.mirror.c_dp] = float(self.x2[1])

    def popUnsetData(self, N):
        """Remove any appened init values from running values"""
        self.r_x1 = self.r_x1[:N]
        self.r_x2 = self.r_x2[:N]
