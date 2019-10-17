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

        self.IACEweight = self.BAdict['IACEweight']

    def step(self):
        # Caclulate ACE
        deltaw = 1.0 - self.mirror.cv['f']

        self.cv['ACETL'] = self.Area.cv['IC'] - self.Area.cv['IC0']

        # B is handled as a positive, though it 'is' a negative number #NOTE: removal of fbase scaling
        self.cv['ACEFB'] = -10*self.B*deltaw*self.mirror.fBase # 10 is standard since f in Hz

        ## Calculate ACEdist based on conditionals
        # 'Fully' calculated ACE - Type 0
        self.cv['ACE'] = self.cv['ACETL'] + self.cv['ACEFB']

        if self.AGCtype ==1:
            # only apply Tie Line interchange if same sign as delta w; always send frequency bias
            if np.sign(self.cv['ACETL']) != np.sign(deltaw):
                self.cv['ACE'] = self.cv['ACEFB']

        elif self.AGCtype == 2:
            # only apply ACE if same sign as delta w
            if np.sign(self.cv['ACE']) != np.sign(deltaw):
                self.cv['ACEdist'] = 0

        elif self.AGCtype == 3:
            self.cv['ACE'] = 0
            # Separate Tieline ACE from Frequency bias
            # only apply component if same sign as delta w
            if np.sign(self.cv['ACETL']) == np.sign(deltaw):
                self.cv['ACE'] += self.cv['ACETL']
            if np.sign(self.cv['ACEFB']) == np.sign(deltaw):
                self.cv['ACE'] += self.cv['ACEFB']

        # Handle computing integral of ACE using trapezoidal integration
        # optional window integration agent
        n = self.mirror.cv['dp']
        if self.windowInt:
            self.cv['IACE'] = self.wIntAgent.step(self.cv['ACE'], self.r_ACE[n-1])
        else:
            self.cv['IACE'] += (self.cv['ACE']+self.r_ACE[n-1])/2.0*self.mirror.timeStep

        IACE2add = 0.0
        # Include Integral of ACE
        if self.BAdict['IncludeIACE']:
            # IACE deadband setting
            if (abs(deltaw) >= self.BAdict['IACEdeadband']/self.mirror.simParams['fBase']):
                """ remove weighted and conditional IACE
                if self.BAdict['IACEuseWeight']:
                    # Add to dispatch signal if same sign as freq deviation
                    if self.BAdict['IACEconditional']: ## NOTE: UNTESTED
                        if (np.sign(deltaw) == np.sign(self.cv['IACE'])) and (np.sign(deltaw) == np.sign(self.cv['ACE'])):
                            IACE2add =  self.cv['ACE'] *(1.0-self.IACEweight) + self.cv['IACE'] * float(self.BAdict['IACEscale'])*self.IACEweight
                    else:
                        #IACE not conditional add weighted ACE
                        IACE2add =  self.cv['ACE'] *(1.0-self.IACEweight) + self.cv['IACE'] * float(self.BAdict['IACEscale'])*self.IACEweight
                else:
                """
                # add non weighted, non conditional ACE
                IACE2add =  self.cv['ACE'] + self.cv['IACE']* float(self.BAdict['IACEscale'])


        # Put ACEdist through filter
        if self.filter != None:
            self.cv['SACE'] = self.filter.stepFilter(self.cv['ACE']+IACE2add)
        else:
            self.cv['SACE'] = self.cv['ACE']+IACE2add

        # Gain ACE
        self.cv['ACE2dist'] = self.cv['SACE']*self.ACEgain

        # Check if current time step is an action step
        if (self.mirror.cv['t'] % self.actTime) == 0:
            self.cv['distStep'] = 1
            ACE2dist = self.cv['ACE2dist']

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