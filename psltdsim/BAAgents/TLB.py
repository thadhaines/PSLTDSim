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

        self.IACEweight = self.BAdict['IACEweight']

    def step(self):
        # Caclulate ACE
        deltaw = self.mirror.cv['f']-1.0
        Pace = self.Area.cv['IC'] - self.Area.cv['IC0']

        # B is handled as a positive, though it 'is' a negative number
        Face = 10*self.B*deltaw*self.mirror.fBase # 10 is standard since f in Hz

        ## Calculate ACEdist based on conditionals
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

        elif self.AGCtype == 3:
            self.cv['ACEdist'] = 0
            # Separate Tieline ACE from Frequency bias
            # only apply component if same sign as delta w
            if np.sign(Pace) == np.sign(deltaw):
                self.cv['ACEdist'] += Pace
            if np.sign(Face) == np.sign(deltaw):
                self.cv['ACEdist'] += Face

        # Handle computing integral of ACE using trapezoidal integration
        n = self.mirror.cv['dp']
        self.cv['ACEint'] += (self.cv['ACE']+self.r_ACE[n-1])/2.0*self.mirror.timeStep

        # optional window integration agent
        if self.windowInt:
            curIACE = self.wIntAgent.step(self.cv['ACE'], self.r_ACE[n-1])
        else:
            curIACE = self.cv['ACEint']

        # Include Integral of ACE
        if self.BAdict['IncludeIACE']:
            # If deltaw larger than deadband setting
            if (abs(deltaw) >= self.BAdict['IACEdeadband']/self.mirror.simParams['fBase']):
                # Add to dispatch signal if same sign as freq deviation
                if self.BAdict['IACEconditional']: ## NOTE: UNTESTED
                    if (np.sign(deltaw) == np.sign(curIACE)) and (np.sign(deltaw) == np.sign(self.cv['ACEdist'])):
                        self.cv['ACEdist'] =  self.cv['ACEdist'] *(1.0-self.IACEweight) + curIACE * float(self.BAdict['IACEscale'])*self.IACEweight
                else:
                    #IACE not conditional add ACE
                    self.cv['ACEdist'] =  self.cv['ACEdist'] *(1.0-self.IACEweight) + curIACE * float(self.BAdict['IACEscale'])*self.IACEweight


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

            # Distribute Ace as a negative
            for gen in self.ctrlMachines:

                if gen.distType.lower() == 'step':
                    if gen.gov_model == False:
                        # distribute Negative ACE to Pmech
                        gen.cv['Pm'] -= ACE2dist*gen.ACEpFactor
                        if gen.cv['Pm'] > gen.Pmax:
                            gen.cv['Pm'] = gen.Pmax
                    else:
                        # distribute Negative ACE % to Pref
                        gen.cv['Pref'] -= ACE2dist*gen.ACEpFactor
                        if gen.cv['Pref'] > gen.Pmax:
                            gen.cv['Pref'] = gen.Pmax

                elif gen.distType.lower() == 'rampa':
                    # Ramp value instead of step
                    if gen.gov_model == False:
                        # distribute Negative ACE to Pmech
                        # NOTE: Don't forget this makese a ton of Agents!
                        if gen.gov_model.mwCap < gen.gov_model.Pref -ACE2dist*gen.ACEpFactor:
                            AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pm',self.mirror.cv['t'],
                                                                  self.actTime, gen.gov_model.mwCap, 'abs'])
                        else:
                            AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pm',self.mirror.cv['t'],
                                                                  self.actTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                        self.mirror.AGCramp.append(AGCramp)
                    else:
                        # distribute Negative ACE % to Pref
                        # NOTE: Don't forget this makese a ton of Agents!
                        if gen.gov_model.mwCap < gen.gov_model.Pref -ACE2dist*gen.ACEpFactor:
                            AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pref',self.mirror.cv['t'],
                                                                  self.actTime, gen.gov_model.mwCap, 'abs'])
                        else:
                            AGCramp = ltd.perturbance.RampAgent(self.mirror, 
                                                            gen, ['Pref',self.mirror.cv['t'],
                                                                  self.actTime, -ACE2dist*gen.ACEpFactor, 'rel'])
                        self.mirror.AGCramp.append(AGCramp)

        else:
            self.cv['distStep'] = 0