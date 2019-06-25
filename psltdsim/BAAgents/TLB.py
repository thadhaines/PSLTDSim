from .BA import BA

class TLB(BA):
    """Tie-Line Bias Balancing Authority Agent derived from generic BA"""
    def __init__(self,mirror, name, BAdict):
        super(TLB, self).__init__(mirror,name,BAdict)

    def step(self):
        # Caclulate ACE
        Pace = self.Area.cv['Pe'] - self.Area.cv['P'] - self.Area.cv['IC0']
        # B is positive
        Face = 10*self.B*(self.mirror.cv['f']-1.0)*self.mirror.fBase # removed 10 since f in Hz
        self.cv['ACE'] = Pace + Face
        
        # Handle running integral of ACE
        self.cv['ACEint'] += self.cv['ACE']

        # Check if current time step is an action step
        if (self.mirror.cv['t'] % self.actTime) == 0:
            self.cv['distStep'] = 1
            # Distribute Ace

            # for each entry in the BA pDict
            for mainPkey in self.pDict:
                # convert main participation to float
                
                fmP = float(mainPkey)
                # for each participation dictionary list entry
                for pEntry in range(len(self.pDict[mainPkey])):

                    # check if power plant
                    if isinstance(self.pDict[mainPkey][pEntry], ltd.systemAgents.PowerPlantAgent):
                        # for each % entry in the PP pDict
                        for subPkey in self.pDict[mainPkey][pEntry].pDict:
                            # convert sub participation to float
                            fsP = float(subPkey)

                            # for each gen in participation group
                            for PPgen in self.pDict[mainPkey][pEntry].pDict[subPkey]:
                                # check if gov model exists
                                if PPgen.gov_model == False:
                                    # if so distribute Negative ACE to Pmech
                                    PPgen.cv['Pm'] -= self.cv['ACE']*fmP*fsP
                                else:
                                    # else distribute Negative ACE % to Pref
                                    PPgen.cv['Pref'] -= self.cv['ACE']*fmP*fsP
                    else:
                        # No Power Plants in BA
                        # for each % entry in BA pDict
                        BAgen = self.pDict[mainPkey][pEntry]
                        # check if gov model exists
                        if BAgen.gov_model == False:
                            # if so distribute Negative ACE to Pmech
                            BAgen.cv['Pm'] -= self.cv['ACE']*fmP
                        else:
                            # else distribute Negative ACE % to Pref
                            BAgen.cv['Pref'] -= self.cv['ACE']*fmP

        else:
            self.cv['distStep'] = 0