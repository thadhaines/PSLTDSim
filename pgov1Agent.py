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
        self.Mbase = self.Gen.MbaseSAV 

        self.K = -10*self.Mbase / model.Sbase / self.droop

    def stepDynamics(self):
        """ Perform drooop control"""
        self.Gen.Pm = self.Gen.Pm + self.K*self.model.c_deltaF

    def stepInitDynamics(self):
        """ Once H has been initialized, check to see if K has to be recalculated"""
        # TODO: recheck for different DYD base after H has been init 
        pass

