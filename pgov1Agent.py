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

        self.Gen = findGenOnBus(model, self.Busnum, self.Id)
        #TODO: handle not finding the gen better.
        if self.Gen:
            self.Mbase = self.Gen.MbaseSAV 
            #Unsure about propber VAbase to use- mbase or sbase?
            self.K = -1*self.model.Sbase / self.droop

    def stepDynamics(self):
        """ Perform droop control"""
        #NOTE: based off of change in f between steps, not system f
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
            self.K = -1*self.model.Sbase / self.droop
            print('updated model.')
            return
        print('nothing updated.')

