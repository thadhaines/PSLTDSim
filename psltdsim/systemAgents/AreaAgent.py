class AreaAgent(object):
    """Area Agent for LTD Model Collections"""
    #NOTE: Account for zones in the future?

    def __init__(self, model, areaNum):
        #from __main__ import col
        # Model Reference
        self.model = model

        # Identification
        self.Area = areaNum

        # Case Parameters
        self.Ngen = len(col.GeneratorDAO.FindByArea(self.Area))
        self.Nload = len(col.LoadDAO.FindByArea(self.Area))

        # Children
        self.Gens = []
        self.Load = []
        self.Slack = []
        self.Machines = []
        self.Bus = []
        # if this is how shunts/SVDs work...
        self.Shunt = []
        self.SVD = []

    def getDataDict(self):
        """Return collected data in dictionary form"""
        d = {'AreaNum': self.Area,
             'Ngen': self.Ngen,
             'Nload': self.Nload,
             }
        return d

    def checkArea(self):
        """Checks if found number of Generators and loads is Correct
        Creates Machine list
        Returns 0 if all valid, -1 for invalid Generators, -2 for invalid loads
        """
        # Q: check for SVD & shunts?
        self.Machines = self.Slack + self.Gens

        if self.Ngen == (len(self.Machines)):
            if self.model.debug: 
                print("Gens correct in Area:\t%d" % self.Area)
            
        else:
            print("*** Gen Error: %d/%d found. Area:\t%d" % 
                  (len(self.Machines), self.Ngen, self.Area))
            return -1

        if self.Nload == len(self.Load):
            if self.model.debug: 
                print("Load correct in Area:\t%d" % self.Area)
        else:
            print("*** Load Error: %d/%d found. Area:\t%d" % 
                  (len(self.Load), self.Nload, self.Area))
            return -2

        return 0