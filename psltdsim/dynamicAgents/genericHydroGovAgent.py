""" Dynamic Agent Class created from generic PSLF prime mover data"""
from .genericGovAgent import genericGovAgent
class genericHydroGovAgent(genericGovAgent):
    """Agent to perform governor action
    Outputs Pmech - accounts for limiting valve and mwcap action
    """

    def __init__(self, mirror, PSLFgov):
        super().__init__( mirror, PSLFgov)

        # Generic Hydro Values 
        self.Ts = 0.4 # Ts
        self.Tc = 45.0 # Tc
        self.T3 = 5.00 # T3
        self.T4 = -1.0 # T4
        self.T5 = 0.5 # T5

        # Dynamic init
        self.sys1 = sig.StateSpace([-1.0/self.Ts],[1.0/self.Ts],
                                   [1.0],0.0)

        self.sys2 = sig.StateSpace([-1.0/self.Tc],[1.0/self.Tc],
                                   [1.0-self.T3/self.Tc],[self.T3/self.Tc])

        self.sys3 = sig.StateSpace([-1.0/self.T5],[1.0/self.T5],
                                   [1.0-self.T4/self.T5],[self.T4/self.T5])

        if mirror.debug:
            print("*** Added Generic Hydro Gov to gen on bus %d '%s'" 
                  % (self.Busnum,self.Busnam))