"""Place for Pertrubance Agents"""

class LoadStepAgent(object):
    """Performs steps of P, Q, or St on Loads - calculates Perturbance deltas
    targetObj is a python mirror agent object reference
    perParams is a list: [targetAttr, tStart, newVal]
    """

    def __init__(self, model, targetObj, perParams):
        self.ProcessFlag = 1

        self.model = model
        self.mObj = targetObj

        self.attr = perParams[0]
        self.tStart = perParams[1]
        self.newVal = perParams[2]

    def step(self):

        if self.ProcessFlag:
            if self.model.c_t < self.tStart:
                # acts as a pass
                return

            if self.model.c_t >= self.tStart:
                # Perform step
                # Get most recent PSLF reference
                self.pObj = self.mObj.getPref()
                #Update correct attribute in PSLF
                if self.attr == 'St':
                    if self.newVal == 1:
                        self.pObj.SetInService()
                        self.model.ss_Pert_Pdelta += self.pObj.P
                        self.model.ss_Pert_Qdelta += self.pObj.Q
                    else:
                        self.pObj.SetOutOfService()
                        self.model.ss_Pert_Pdelta -= self.pObj.P
                        self.model.ss_Pert_Qdelta -= self.pObj.Q

                elif self.attr == 'P':
                    oldVal = self.pObj.P
                    self.pObj.P = self.newVal
                    self.model.ss_Pert_Pdelta += self.newVal - oldVal

                elif self.attr == 'Q':
                    oldVal = self.pObj.Q
                    self.pObj.Q = self.newVal
                    self.model.ss_Pert_Qdelta += self.newVal - oldVal

                # Save Changes in PSLF
                self.pObj.Save()
                # Update mirror
                self.mObj.getPvals()

                self.ProcessFlag = 0
                if self.model.debug:
                    # TODO: Make this output more informative
                    print("Load Step on Bus %d Processed" % self.mObj.Bus.Extnum )
                return