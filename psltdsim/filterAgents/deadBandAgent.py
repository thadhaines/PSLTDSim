class deadBandAgent():
    """Agent to be used as a customizable governor deadband."""

    def __init__(self, mirror, parentAgent, BAdict):
    #def __init__(self, fBase, R, BAdict): # for debug
        #self.fBase = fBase
        #self.R = R
        # parentAgent a governor with an R value

        self.mirror = mirror
        self.parentAgent = parentAgent
        self.BAdict = BAdict
        self.fBase = mirror.fBase

        self.R = parentAgent.R

        self.dbType = 0

        if self.BAdict['GovDeadbandType'] == 'step':
            self.dbType = 1
            self.dbPu = self.BAdict['GovDeadband']/self.fBase
            self.wOffset = 0.0

        elif self.BAdict['GovDeadbandType'] == 'ramp':
            self.dbType = 2
            self.dbPu =  self.BAdict['GovDeadband']/self.fBase
            self.R2 = self.R-self.dbPu # Calculate new R
            self.wOffset = self.dbPu

        elif self.BAdict['GovDeadbandType'] == 'NLDroop':
            # Non-linear droop i.e. Compound R
            self.dbType = 3
            self.alpha = self.BAdict['GovAlpha']/self.fBase
            self.beta  = self.BAdict['GovBeta']/self.fBase

            # ensure alpha < beta
            if self.alpha > self.beta:
                tempVal = self.beta
                self.beta = self.alpha
                self.alpha = tempVal

            self.R3 = -(self.alpha-self.beta)/(self.beta/self.R) # calculate new R
            self.wOffset = self.alpha

    def step(self, delta_w):
        """ Perform desired deadband operation, return delta_w and R - Both PU """
        outputR = self.R

        # Step type Deadband
        if self.dbType == 1:
            if abs(delta_w) < (self.dbPu):
                delta_w = 0

        # Ramp Deadband
        if self.dbType == 2:
            outputR = self.R2
            if abs(delta_w) < (self.dbPu):
                delta_w = 0
            # Shifting of w
            elif delta_w > 0:
                delta_w -= self.wOffset
            else:
                delta_w += self.wOffset

        # Non-linear Droop
        if self.dbType == 3:
        # standard deadband using alpha as db limit
            if abs(delta_w) <= (self.alpha):
                delta_w = 0
            # Shift the w to edge of deadband if less than beta, select R
            else:
                if delta_w > 0 and abs(delta_w) < self.beta:
                    delta_w -= self.alpha
                    outputR = self.R3
                elif delta_w < 0 and abs(delta_w) < self.beta:
                    delta_w += self.alpha
                    outputR = self.R3

        return (delta_w, outputR)