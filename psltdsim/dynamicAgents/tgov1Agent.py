""" Dynamic Agent Class created from PSLF machine data"""

class tgov1Agent():
    """Agent to perform governor action
    Outputs Pmech - accounts for limiting valve and mwcap action
    """

    def __init__(self, mirror, PSLFgov):
        """Objects created from intPY3Dynamics"""
        self.mirror = mirror
        self.PSFLgov = PSLFgov
        self.Gen = PSLFgov.Gen
        self.Pref = self.Gen.Pset

        self.appenedData = True

        self.Busnum = PSLFgov.Busnum
        self.Busnam = PSLFgov.Busnam
        self.baseKv = PSLFgov.Base_kV
        self.Id = PSLFgov.Id
        
        self.mwCap = PSLFgov.mwCap # default behavior - over written during dynamic init
        self.Mbase = self.Gen.Mbase

        self.R  = PSLFgov.R
        self.T1 = PSLFgov.T1
        self.Vmax = PSLFgov.Vmax
        self.Vmin = PSLFgov.Vmin
        self.T2 = PSLFgov.T2 # in sec
        self.T3 = PSLFgov.T3
        self.Dt = PSLFgov.Dt

        self.t = [0 , self.mirror.timeStep] # will have to be moved if ts = variable

        # Dynamic init
        self.sys1 = sig.StateSpace([-1.0/self.T1],[1.0/self.T1],
                                   [1.0],0.0)
        self.sys2 = sig.StateSpace([-1.0/self.T3],[1.0/self.T3],
                                   [1.0-self.T2/self.T3],[self.T2/self.T3])

        if mirror.debug:
            print("*** Added tgov1 to gen on bus %d '%s'" 
                  % (self.Busnum,self.Busnam))

    def stepDynamics(self):
        """ Perform governor control"""
        self.Pref = self.Gen.Pset # get newest set value.

        # Create system inputs
        delta_w = 1.0-self.mirror.c_f
        PrefVec = np.array([self.Pref,self.Pref])
        dwVec = np.array([delta_w,delta_w])/self.R*self.Mbase

        # Perform sum and first gain block
        uVector = (PrefVec+dwVec)

        # First dynamic Block
        _, y1, self.x1 = sig.lsim(self.sys1, U=uVector, T=self.t, 
                                   X0=self.r_x1[self.mirror.c_dp-1], interp=True)
        ys = y1

        # limit Valve position (i.e. Pm out)
        for x in range(2):
            if ys[x]>self.y1HighLimit:
                ys[x] = self.y1HighLimit
            elif ys[x]<self.y1LowLimit:
                ys[x] = self.y1LowLimit

        # Second block
        _, y2, self.x2 = sig.lsim(self.sys2, y1, T=self.t,
                                   X0=self.r_x2[self.mirror.c_dp-1], interp=True)
        self.mirror.DynamicSolns += 2

        # Accout for damping
        Pmech = y2[1] - delta_w*self.Dt*self.Mbase

        # Set Generator Mechanical Power
        self.Gen.Pm = float(Pmech) # float because y2 is numpy ....

    def stepInitDynamics(self):
        """ set Pm = Pe, calculate MW limits of valve position"""
        self.Gen.Pm = self.Gen.Pe
        self.Gen.Pset = self.Gen.Pe
        
        updated = False
        if self.mirror.debug:
            print('*** Checking for updated model information for %d %s...' 
                  % (self.Gen.Busnum, self.Gen.Busnam))

        # ensure MWcap is read from gov dyd
        if self.Gen.Pmax != self.mwCap:
            if self.mirror.debug:
                print('... updated mwCap from %.2f to %.2f' %
                      (self.Gen.Pmax, self.mwCap) )
            self.Gen.Pmax = self.mwCap
            updated = True

        # Ensure correct limiting values
        self.y1HighLimit = self.Vmax * self.mwCap
        self.y1LowLimit = self.Vmin * self.mwCap

        if self.mirror.debug and not updated:
            print('... nothing updated.')
            return

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
