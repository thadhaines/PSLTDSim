"""Place for Pertrubance Agents"""

class LoadStepAgent(object):
    """Used for steps of P,Q, or St on Loads
    targetObj is a python mirror agent object reference
    targetAttr is a string ( 'P' 'Q' 'St' )
    """

    def __init__(self, model, targetObj, perParams):
        self.ProcessFlag = 1
        self.model = model
        self.mObj = targetObj
        self.pObj = targetObj.getPref()
        self.attr = perParams[0]
        self.tStart = perParams[1]
        self.newVal = perParams[2]

    def step(self):

        if self.ProcessFlag:
            if self.model.c_t < self.tStart:
                return
            if self.model.c_t >= self.tStart:
                #Update correct attribute in mirror and PSLF
                if self.attr == 'St':
                    self.mObj.St = self.newVal
                    self.pObj.St = self.newVal
                elif self.attr == 'P':
                    self.mObj.P = self.newVal
                    self.pObj.P = self.newVal
                elif self.attr == 'Q':
                    self.mObj.Q = self.newVal
                    self.pObj.Q = self.newVal

                # Save Changes in PSLF
                # NOTE: getPval of agents will have to refresh P Q and St each step
                self.pObj.Save()
                self.ProcessFlag = 0
                if self.model.debug:
                    print("Load Step on Bus %d Processed" % self.mObj.Bus.Extnum )
                return