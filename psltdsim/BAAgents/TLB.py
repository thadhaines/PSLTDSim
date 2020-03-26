from .BA import BA

class TLB(BA):
    """Tie-Line Bias Balancing Authority Agent derived from generic BA"""
    def __init__(self,mirror, name, BAdict):
        super(TLB, self).__init__(mirror,name,BAdict)

        # Handle different types of TLB
        typeSTR = self.BAdict['AGCType'].split(":")
        if len(typeSTR)>1:
            self.AGCtype = int(typeSTR[1])
        else:
            self.AGCtype = 0

        if self.BAdict['IACEwindow'] > 0:
            # create window integrator if window lengtht exists
            self.wIntAgent = ltd.systemAgents.WindowIntegratorAgent(
                self.mirror, self.BAdict['IACEwindow'])
            self.windowInt = True
        else:
            self.windowInt = False

        # Use ACEgain if applicable
        if 'ACEgain' in self.BAdict:
            self.ACEgain = self.BAdict['ACEgain']
        else:
            self.ACEgain = 1.0

        # handle none and 0 equivalence
        if type(self.BAdict['AGCDeadband']) == type(None):
            self.BAdict['AGCDeadband'] = 0.0


    def step(self):
        # Caclulate ACE
        deltaw = 1.0 - self.mirror.cv['f']
        # Calculate Variable Frequency Bias
        self.cv['Bv'] = self.B*( 1+self.BVgain* abs(deltaw) )

        self.cv['ACETL'] = self.Area.cv['IC'] - self.Area.cv['IC0']

        # B is handled as a positive, though it 'is' a negative number #NOTE: removal of fbase scaling
        self.cv['ACEFB'] = -10*self.B*deltaw*self.mirror.fBase # 10 is standard since f in Hz

        # Handling of optional gain
        variableFbias = -10* self.cv['Bv']*deltaw*self.mirror.fBase # 10 is standard since f in Hz

        ## Calculate ACEdist based on conditionals
        # Reporting ACE - per WECC mandate
        self.cv['RACE'] = self.cv['ACETL'] + self.cv['ACEFB']

        # Conditional ACE used for distribution (type 0 calculation)
        condACE = self.cv['ACETL'] + variableFbias

        if self.AGCtype ==1:
            # only apply Tie Line interchange if same sign as delta w; always send frequency bias
            if np.sign(self.cv['ACETL']) != np.sign(deltaw):
                condACE = variableFbias

        elif self.AGCtype == 2:
            # only apply ACE if same sign as delta w
            if np.sign(condACE) != np.sign(deltaw):
                condACE = 0

        elif self.AGCtype == 3:
            condACE = 0
            # Separate Tieline ACE from Frequency bias
            # only apply component if same sign as delta w
            if np.sign(self.cv['ACETL']) == np.sign(deltaw):
                condACE += self.cv['ACETL']
            if np.sign(variableFbias) == np.sign(deltaw):
                condACE += variableFbias

        elif self.AGCtype == 4:
            # only send ace if summation is same sign as frequency deviation
            if np.sign(condACE) == np.sign(deltaw):
                condACE = 0

        self.cv['condACE'] = condACE

        # Handle computing integral of ACE using trapezoidal integration
        # optional window integration agent
        n = self.mirror.cv['dp']
        #Window integration using Reported ACE -> Makes sense as AGC should bring RACE to Zero
        if self.windowInt:
            self.cv['IACE'] = self.wIntAgent.step(self.cv['RACE'], self.r_RACE[n-1])
        else:
            self.cv['IACE'] += (self.cv['RACE']+self.r_RACE[n-1])/2.0*self.mirror.timeStep
        """
        # Window integration using conditional ACE
        if self.windowInt:
            self.cv['IACE'] = self.wIntAgent.step(self.cv['condACE'], self.r_condACE[n-1])
        else:
            self.cv['IACE'] += (self.cv['condACE']+self.r_condACE[n-1])/2.0*self.mirror.timeStep
        """

        IACE2add = 0.0
        # Include Integral of ACE
        if self.BAdict['IncludeIACE']:
            # IACE deadband setting
            if (abs(deltaw) >= self.BAdict['IACEdeadband']/self.mirror.simParams['fBase']):
                # add non weighted, non conditional ACE
                IACE2add =  self.cv['IACE']* float(self.BAdict['IACEscale'])

        if self.BAdict['IACEconditional']:
            if np.sign(IACE2add) == np.sign(deltaw):
                IACE2add = 0

        # Put ACEdist through filter
        if self.filter != None:
            self.cv['SACE'] = self.filter.stepFilter(condACE+IACE2add)
        else:
            self.cv['SACE'] = condACE+IACE2add

        # Gain ACE
        self.cv['condACE'] = condACE # for logical logging purposes
        self.cv['ACE2dist'] = self.cv['SACE']*self.ACEgain
        self.cv['distStep'] = 0 # changed in ltd.agc.distACE if appropriate

        # Check if current time step is an action step
        #TODO: add option to be triggered via DTC action...
        if (self.mirror.cv['t'] % self.actTime) == 0:

            # check deadband qualifications if set
            if self.BAdict['AGCDeadband'] > 0:
                # NOTE: could be set to BAAL...
                if abs(self.cv['ACE2dist']) >= self.BAdict['AGCDeadband']:
                    ltd.agc.distACE(self)
            else:
                # No Deadband
                ltd.agc.distACE(self)
