""" Dynamic Agent Class created from dyd information"""

class pgov1Agent():
    """Agent to perform proportional governor action (droop)"""

    def __init__(self, model, cleanLine):
        """Objects created from parseDyd, cleanLine is list of parameters"""
        self.model = model
        self.cleanLine = cleanLine

        self.Busnum = cleanLine[1]
        self.Busnam = cleanLine[2]
        self.baseKv = cleanLine[3]
        self.Id = cleanLine[4]
        
        self.mwCap = float(cleanLine[6].split("=")[1])
        self.droop = cleanLine[7]
        self.k1 = cleanLine[8]

        self.Gen = findGenOnBus(model, self.Busnum, self.Id)
        #TODO: handle not finding the gen better.
        if self.Gen:
            self.Mbase = self.Gen.MbaseSAV 
            self.K = -self.k1*self.Mbase / self.model.Sbase / self.droop

    def stepDynamics(self):
        """ Perform droop control"""
        #NOTE: based off of change in f between steps, not system f
        """
        deltaOmega = 1 - self.model.c_f

        if self.model.c_deltaF != 0.0:
            damping = (self.Gen.Pm-self.Gen.r_Pm[self.model.c_dp-1])/self.model.c_deltaF

        else:
            damping = 0.0

        possiblePm = self.Gen.Pm + self.K*deltaOmega - damping
        """
        possiblePm = self.Gen.Pm + self.K*self.model.c_deltaF
        if possiblePm <= self.mwCap:
            self.Gen.Pm = possiblePm
        else:
            self.Gen.Pm = self.mwCap

    def stepInitDynamics(self):
        """ Once H has been initialized, check if K has to be recalculated"""

        print('Checking for updated model information...')

        if self.Gen.MbaseSAV != self.Gen.MbaseDYD:
            self.Mbase = self.Gen.MbaseDYD
            self.K = -1*k1*self.Mbase / self.model.Sbase / self.droop
            print('updated model.')
            return
        print('nothing updated.')

