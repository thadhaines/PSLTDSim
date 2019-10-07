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

        if self.BAdict['IACEwidow'] > 0:
            # create window integrator if window lengtht exists
            self.wIntAgent = ltd.systemAgents.WindowIntegratorAgent(
                self.mirror, self.BAdict['IACEwidow'])
            self.windowInt = True
        else:
            self.windowInt = False

    def step(self):
        # Caclulate ACE
        deltaw = self.mirror.cv['f']-1.0
        Pace = self.Area.cv['IC'] - self.Area.cv['IC0']

        # B is handled as a positive, though it 'is' a negative number
        Face = 10*self.B*deltaw*self.mirror.fBase # 10 is standard since f in Hz

        # 'Fully' calculated ACE
        self.cv['ACE'] = Pace + Face

        if self.AGCtype == 0:
            self.cv['ACEdist'] = self.cv['ACE']

        elif self.AGCtype ==1:
            # only apply Tie Line interchange if same sign as delta w; always send frequency bias
            if np.sign(Pace) == np.sign(deltaw):
                self.cv['ACEdist'] = self.cv['ACE']
            else:
                self.cv['ACEdist'] = Face

        elif self.AGCtype == 2:
            # only apply ACE if same sign as delta w
            if np.sign(self.cv['ACE']) == np.sign(deltaw):
                self.cv['ACEdist'] = self.cv['ACE']
            else:
                self.cv['ACEdist'] = 0

        # Handle computing integral of ACE using trapezoidal integration
        n = self.mirror.cv['dp']
        self.cv['ACEint'] += (self.cv['ACE']+self.r_ACE[n-1])/2.0*self.mirror.timeStep

        # handle optional window integration agent
        if self.windowInt:
            curIACE = self.wIntAgent.step(self.cv['ACE'], self.r_ACE[n-1])
        else:
            curIACE = self.cv['ACEint']

        # Include Integral of ACE
        if self.BAdict['IncludeIACE']:
            # If deltaw larger than deadband setting
            if (abs(deltaw) >= self.BAdict['IACEdeadband']/self.mirror.simParams['fBase']):
                # Add to dispatch signal if same sign as freq deviation
                self.cv['ACEdist'] += curIACE * float(self.BAdict['IACEscale'])
                #if np.sign(deltaw) == np.sign(curIACE):
        """
        # attempts at resolving steady state ACE
        if abs(deltaw) <= self.BAdict['IACEdeadband']/self.mirror.simParams['fBase']*.8 :# deltaw 2x less than deadband
            # send IACE if less than arbitrary limit, and helpful to ACE
            if abs(self.cv['ACE']) <= 5.0 and np.sign(self.cv['ACEdist']) == np.sign(curIACE):
                self.cv['ACEdist'] += curIACE / self.wIntAgent.windowSize
        """

        # Put ACEdist through filter
        if self.filter != None:
            self.cv['ACEfilter'] = self.filter.stepFilter(self.cv['ACEdist'])
            ACE2dist = self.cv['ACEfilter']
        else:
            ACE2dist = self.cv['ACEdist']

        # Check if current time step is an action step
        if (self.mirror.cv['t'] % self.actTime) == 0:
            self.cv['distStep'] = 1
            # Distribute Ace

            for gen in self.ctrlMachines:
                if gen.distType.lower() == 'step':
                    if gen.gov_model == False:
                        # distribute Negative ACE to Pmech
                        gen.cv['Pm'] -= ACE2dist*gen.ACEpFactor
                    else:
                        # distribute Negative ACE % to Pref
                        gen.cv['Pref'] -= ACE2dist*gen.ACEpFactor

                elif gen.distType.lower() == 'rampa':
                    # Ramp value instead of step
                    if gen.gov_model == False:
                        # distribute Negative ACE to Pmech
                        # NOTE: Don't forget this makese a ton of Agents!
                        AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pm',self.mirror.cv['t'],
                                                                  self.actTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                        self.mirror.AGCramp.append(AGCramp)
                    else:
                        # distribute Negative ACE % to Pref
                        # NOTE: Don't forget this makese a ton of Agents!
                        AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pref',self.mirror.cv['t'],
                                                                  self.actTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                        self.mirror.AGCramp.append(AGCramp)

        else:
            self.cv['distStep'] = 0