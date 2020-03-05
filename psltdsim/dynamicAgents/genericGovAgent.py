""" Dynamic Agent Class created from generic PSLF prime mover data
Handles all dynamic action associated with generic governor 
Specific time constants and state space models created in named generics
"""

class genericGovAgent(object):
    """Agent to perform governor action
    Outputs Pmech - accounts for limiting valve and mwcap action
    """

    def __init__(self, mirror, PSLFgov):
        """Objects created from intPY3Dynamics"""
        self.mirror = mirror
        self.PSLFgov = PSLFgov
        self.Gen = PSLFgov.Gen
        self.Pref = self.Gen.cv['Pref']

        self.appenedData = True

        self.Busnum = PSLFgov.Busnum
        self.Busnam = PSLFgov.Busnam
        self.baseKv = PSLFgov.Base_kV
        self.Id = PSLFgov.Id
        
        self.mwCap = PSLFgov.mwCap # default behavior - over written during dynamic init
        self.Mbase = self.Gen.Mbase

        self.R  = PSLFgov.R 
        # handle if Type ieeeg1 where R is reciprocal
        if PSLFgov.Type == 'ieeeg1':
            self.R = 1/PSLFgov.R
        
        self.Gen.cv['R'] = self.R # workaround until gov.cv dict becomes a thing

        #possibly get from inputs
        self.Vmax = 1.0
        self.Vmin = 0.0
        self.Dt = 0.0

        self.uVector = [0,0]

        # placeholders for optional agents and dictionaries
        self.dbDict = None
        self.delayDict = None
        self.dbAgent = None
        self.wDelay = None
        self.PrefDelay = None

        self.totValveMovement = 0.0

        self.t = [0 , self.mirror.timeStep] # will have to be moved if ts = variable

    def stepDynamics(self):
        """ Perform governor control"""
        self.Pref = self.Gen.cv['Pref'] # get newest set value.
        self.R = self.Gen.cv['R']

        # logical Pref delay block placement
        if self.PrefDelay != None:
            self.Pref = self.PrefDelay.step(self.Gen.cv['Pref'])

        # Create system inputs
        self.w = self.mirror.cv['f']

        # delta_w delay plot placement
        if self.wDelay != None:
            delta_w = self.wDelay.step(1.0-self.w)
        else:
            delta_w = 1.0-self.w

        usableR = self.R

        # handle deadband - step...
        if self.dbAgent is not None:
            delta_w, usableR = self.dbAgent.step(delta_w)

        PrefVec = np.array([self.Pref,self.Pref])
        dwVec = np.array([delta_w,delta_w])/(usableR)*self.Mbase 


        # Perform sum and first gain block
        self.uVector = (PrefVec+dwVec)
        
        # limit input #NOTE: Untested
        for ndx in range(len(self.uVector)):
            if self.uVector[ndx] > self.y1HighLimit:
                self.uVector[ndx] = self.y1HighLimit
            elif self.uVector[ndx] <self.y1LowLimit:
                self.uVector[ndx] = self.y1LowLimit
        

        # First dynamic Block
        _, y1, self.x1 = sig.lsim(self.sys1, U=self.uVector, T=self.t, 
                                   X0=self.r_x1[self.mirror.cv['dp']-1], interp=True)

        # Second block
        _, y2, self.x2 = sig.lsim(self.sys2, y1, T=self.t,
                                   X0=self.r_x2[self.mirror.cv['dp']-1], interp=True)
        # Third Block
        _, y3, self.x3 = sig.lsim(self.sys3, y2, T=self.t,
                                   X0=self.r_x3[self.mirror.cv['dp']-1], interp=True)
        self.mirror.DynamicSolns += 3

        # Accout for damping
        Pmech = y3[1] - delta_w*self.Dt*self.Mbase

        # Set Generator Mechanical Power
        self.Gen.cv['Pm'] = float(Pmech) # float because y is numpy ....

    def stepInitDynamics(self):
        """ set Pm = Pe, calculate MW limits of valve position"""
        self.Gen.cv['Pm'] = self.Gen.cv['Pe']
        self.Gen.cv['Pref'] = self.Gen.cv['Pe']

        self.mirror.ss_Hgov += self.Gen.H
        
        updated = False
        if self.mirror.debug:
            print('*** Checking for updated model information for %d %s...' 
                  % (self.Gen.Busnum, self.Gen.Busnam))

        # Ensure R is on correct base
        if self.Gen.Mbase != self.mwCap:
            Rnew = self.R*self.Gen.Mbase/self.mwCap
            if self.mirror.debug:
                print('... updated R from %.4f to %.4f' %
                      (self.R, Rnew) )
            self.R = Rnew
            updated = True

        # ensure MWcap is read from gov dyd
        if self.Gen.Pmax != self.mwCap:
            if self.mirror.debug:
                print('... updated mwCap from %.2f to %.2f' %
                      (self.Gen.Pmax, self.mwCap) )
            self.Gen.Pmax = self.mwCap
            updated = True

        # Ensure correct limiting values
        # assume no odd limits in generic govs
        self.y1HighLimit =self.mwCap
        self.y1LowLimit = 0.0

        # Ensure correct BA settings
        if self.Gen.AreaAgent.BA:
            if self.Gen.AreaAgent.BA.BAdict['UseAreaDroop']:
                self.R = self.Gen.AreaAgent.BA.BAdict['AreaDroop']
            # Generator belongs to a BA, check if deadband set
            if 'GovDeadband' in self.Gen.AreaAgent.BA.BAdict:
                self.dbAgent = ltd.filterAgents.deadBandAgent(self.mirror, self, self.Gen.AreaAgent.BA.BAdict)

        # Create Overwriting individual deadband (if applicable)
        if self.dbDict != None:
            # dbDict present, overwrite BA defined deadband
            self.dbAgent = ltd.filterAgents.deadBandAgent(self.mirror, self, self.dbDict)

        # Init delays if available
        if self.delayDict != None:
            # check for delta w delay if any non zero dealy,filter values or gain value entered
            if ( any(self.delayDict['wDelay'][0:2]) > 0 ) or (len(self.delayDict['wDelay']) > 2):
                initVal = 0.0
                newDelay = ltd.filterAgents.delayAgent(self, self.mirror, initVal, self.delayDict['wDelay'],)
                # place delay link into mirror delay list
                newDelay.offSet = 0
                self.mirror.Delay.append(newDelay)
                self.wDelay = newDelay

            # check for PrefDelay
            if (any(self.delayDict['PrefDelay'][0:2]) > 0) or (len(self.delayDict['PrefDelay']) > 2):
                initVal = self.Pref
                newDelay = ltd.filterAgents.delayAgent(self, self.mirror, initVal, self.delayDict['PrefDelay'],)
                # place delay link into mirror delay list
                newDelay.offSet = 1
                self.mirror.Delay.append(newDelay)
                self.PrefDelay = newDelay
        if self.mirror.debug and not updated:
            print('... nothing updated.')
            return

    def initRunningVals(self):
        """Initialize History Values of dynamic agent"""
        # History Values
        self.r_x1 = [0.0]*self.mirror.dataPoints
        self.r_x2 = [0.0]*self.mirror.dataPoints
        self.r_x3 = [0.0]*self.mirror.dataPoints
        self.r_u = [0.0]*self.mirror.dataPoints
        self.r_w = [0.0]*self.mirror.dataPoints
        self.r_Pref = [0.0]*self.mirror.dataPoints
        self.r_valveTravel = [0.0]*self.mirror.dataPoints

        # Append init values to running state data
        self.r_x1.append(self.Gen.cv['Pm'])
        self.r_x2.append(self.Gen.cv['Pm'])
        self.r_x3.append(self.Gen.cv['Pm'])

    def logStep(self):
        """Update Log information"""
        self.r_x1[self.mirror.cv['dp']] = float(self.x1[1])
        self.r_x2[self.mirror.cv['dp']] = float(self.x2[1])
        self.r_x3[self.mirror.cv['dp']] = float(self.x3[1])
        self.r_u[self.mirror.cv['dp']] = float(self.uVector[0])
        self.r_u[self.mirror.cv['dp']] = float(self.uVector[0])
        self.r_w[self.mirror.cv['dp']] = self.w
        self.r_Pref[self.mirror.cv['dp']] = self.Pref
        self.totValveMovement += abs( self.r_x1[self.mirror.cv['dp']] - self.r_x1[self.mirror.cv['dp']-1])/self.mwCap
        self.r_valveTravel[self.mirror.cv['dp']] = self.totValveMovement

    def popUnsetData(self, N):
        """Remove any appened init values from running values"""
        self.r_x1 = self.r_x1[:N]
        self.r_x2 = self.r_x2[:N]
        self.r_x3 = self.r_x3[:N]
        self.r_u = self.r_u[:N]
        self.r_w = self.r_w[:N]
        self.r_Pref = self.r_Pref[:N]
        self.r_valveTravel = self.r_valveTravel[:N]


    def setState(self, newState):
        """ When stepping Pm, states must be reset"""
        self.x1[1] = newState
        self.x2[1] = newState
        self.x3[1] = newState