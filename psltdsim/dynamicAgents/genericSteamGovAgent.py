""" Dynamic Agent Class created from generic PSLF prime mover data"""
from .genericGovAgent import genericGovAgent

class genericSteamGovAgent(genericGovAgent):
    """Agent to perform governor action
    Outputs Pmech - accounts for limiting valve and mwcap action
    """

    def __init__(self, mirror, PSLFgov):
        """Objects created from intPY3Dynamics"""
        super().__init__( mirror, PSLFgov)
        # Generic Steam Values 
        self.Ts = 0.04 # Ts
        self.Tc = 0.20 # Tc
        self.T3 = 0.00 # T3
        self.T4 = 1.5 # T4
        self.T5 = 5.0 # T5


        # Dynamic init
        self.sys1 = sig.StateSpace([-1.0/self.Ts],[1.0/self.Ts],
                                   [1.0],0.0)

        self.sys2 = sig.StateSpace([-1.0/self.Tc],[1.0/self.Tc],
                                   [1.0-self.T3/self.Tc],[self.T3/self.Tc])

        self.sys3 = sig.StateSpace([-1.0/self.T5],[1.0/self.T5],
                                   [1.0-self.T4/self.T5],[self.T4/self.T5])

        if mirror.debug:
            print("*** Added Generic Steam Gov to gen on bus %d '%s'" 
                  % (self.Busnum,self.Busnam))
