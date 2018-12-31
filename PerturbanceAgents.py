"""Place for Pertrubance Agents"""

class LoadStepAgent(object):
    """Used for steps of P, Q, or St on Loads
    targetObj is a python mirror agent object reference
    perParams is a list: [targetAttr, tStart, newVal]
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
                #Update correct attribute in PSLF
                if self.attr == 'St':
                    if self.newVal == 1:
                        self.pObj.SetInService()
                    else:
                        self.pObj.SetOutOfService()

                elif self.attr == 'P':
                    self.pObj.P = self.newVal
                    self.pObj.SetInService()
                elif self.attr == 'Q':
                    self.pObj.Q = self.newVal
                    self.pObj.SetInService()

                # Save Changes in PSLF
                self.pObj.Save()
                # Update mirror
                self.mObj.getPvals()

                self.ProcessFlag = 0
                if self.model.debug:
                    print("Load Step on Bus %d Processed" % self.mObj.Bus.Extnum )
                return