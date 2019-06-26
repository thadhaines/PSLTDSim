from .BA import BA

class TLB(BA):
    """Tie-Line Bias Balancing Authority Agent derived from generic BA"""
    def __init__(self,mirror, name, BAdict):
        super(TLB, self).__init__(mirror,name,BAdict)

    def step(self):
        # Caclulate ACE
        Pace = self.Area.cv['Pe'] - self.Area.cv['P'] - self.Area.cv['IC0']
        # B is positive
        Face = 10*self.B*(self.mirror.cv['f']-1.0)*self.mirror.fBase # 10 is standard since f in Hz

        self.cv['ACE'] = Pace + Face
        
        # Handle running integral of ACE using trapezoidal integration
        n = self.mirror.cv['dp']
        self.cv['ACEint'] += (self.cv['ACE']+self.r_ACE[n-1])/2.0*self.mirror.timeStep

        # Deal with filtering
        if self.filter != None:
            self.cv['ACEfilter'] = self.filter.stepFilter(self.cv['ACE'])
            ACE2dist = self.cv['ACEfilter']
        else:
            ACE2dist = self.cv['ACE']

        # Check if current time step is an action step
        if (self.mirror.cv['t'] % self.actTime) == 0:
            self.cv['distStep'] = 1
            # Distribute Ace

            for gen in self.ctrlMachines:
                if gen.gov_model == False:
                    # distribute Negative ACE to Pmech
                    gen.cv['Pm'] -= ACE2dist*gen.ACEpFactor
                else:
                    # distribute Negative ACE % to Pref
                    gen.cv['Pref'] -= ACE2dist*gen.ACEpFactor

        else:
            self.cv['distStep'] = 0