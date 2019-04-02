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
        
        self.mwCap = self.Gen.MbaseDYD # default PSLF behaviour

        self.R  = PSLFgov.R
        self.T1 = PSLFgov.T1
        self.Vmax = PSLFgov.Vmax
        self.Vmin = PSLFgov.Vmin
        self.T2 = PSLFgov.T2 # in sec
        self.T3 = PSLFgov.T3
        self.Dt = PSLFgov.Dt

        self.t = [0 , self.mirror.timeStep]

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
        Pref = self.Gen.Pe * self.R
        delta_w = self.mirror.c_deltaF

        PrefVec = np.array([Pref]*2)
        dwVec = np.array([delta_w]*2)

        # Perform sum and first gain block
        uVector = (PrefVec-dwVec)/self.R

        # First dynamic Block
        _, y1, self.x1 = sig.lsim(self.sys1, U=uVector, T=self.t, 
                                   X0=self.r_x1[self.mirror.c_dp-1]) # this intit value should be a histroy of x1
        ys = y1

        # limit Valve position (i.e. Pm out)
        for x in range(ys.size):
            if ys[x]>self.y1HighLimit:
                ys[x] = self.y1HighLimit
            elif ys[x]<self.y1LowLimit:
                ys[x] = self.y1LowLimit

        # Second block
        _, y2, self.x2 = sig.lsim(self.sys2, ys, T=self.t, 
                                   X0=self.r_x2[self.mirror.c_dp-1]) # this initial value should be okay...

        # Addition of damping
        Pmech = y2 - dwVec*self.Dt

        # Set Generator Mechanical Power
        self.Gen.Pm = float(Pmech[1])

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
        self.r_x1.append(self.Gen.Pm)
        self.r_x2.append(self.Gen.Pm)

    def logStep(self):
        """Update Log information"""
        self.r_x1[self.mirror.c_dp] = float(self.x1[1])
        self.r_x2[self.mirror.c_dp] = float(self.x2[1])

    def popUnsetData(self, N):
        """Remove any appened init values from running values"""
        self.r_x1 = self.r_x1[:N]
        self.r_x2 = self.r_x2[:N]

