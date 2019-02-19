"""Place for Pertrubance Agents"""

class LoadStepAgent(object):
    """Performs steps of P, Q, or St on Loads - calculates Perturbance deltas
    targetObj is a python mirror agent object reference
    perParams is a list: [targetAttr, tStart, newVal]
    Updated to NOT save any PSLF objects attached to self.
    """

    def __init__(self, model, targetObj, perParams):
        self.ProcessFlag = 1

        self.model = model
        self.mObj = targetObj

        self.attr = perParams[0]
        self.tStart = perParams[1]
        self.newVal = perParams[2]

        

        if len(perParams) > 3 :
            self.stepType = perParams[3]
        else:
            self.stepType = 'abs'

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Stepping %s on Bus %d at time %.2f to %.2f %s" %(
            self.attr,
            self.mObj.Bus.Extnum,
            self.tStart,
            self.newVal,
            self.stepType,
            )

        return(tag1+tag2)

    def step(self):

        if self.ProcessFlag:
            if self.model.c_t < self.tStart:
                # acts as a pass
                return

            if self.model.c_t >= self.tStart:
                # Perform Perturbance step
                # Get most recent PSLF reference
                pObj = self.mObj.getPref()
                # for EPCL code string
                self.sb = str(pObj.get__Idx())

                # Update correct attribute in PSLF
                if self.attr == 'St':
                    if self.newVal == 1:
                        #pObj.SetInService()
                        pertStr = ("load[%s].st = 1" % self.sb)
                        self.model.ss_Pert_Pdelta += pObj.P
                        self.model.ss_Pert_Qdelta += pObj.Q
                    else:
                        #pObj.SetOutOfService()
                        pertStr = ("load[%s].st = 0" % self.sb)
                        self.model.ss_Pert_Pdelta -= pObj.P
                        self.model.ss_Pert_Qdelta -= pObj.Q

                elif self.attr == 'P':
                    oldVal = pObj.P
                    if self.stepType == 'rel':
                        pObj.P += self.newVal # relative step
                    else:
                        pObj.P = self.newVal # absolute step

                    pertStr = ("load[%s].p = %f" % (self.sb, pObj.P))
                    self.model.ss_Pert_Pdelta += pObj.P - oldVal

                elif self.attr == 'Q':
                    oldVal = pObj.Q
                    pObj.Q = self.newVal
                    pertStr = ("load[%s].q = %f" % (self.sb,pObj.Q))
                    model.ss_Pert_Qdelta += self.newVal - oldVal

                # Save Changes in PSLF
                #pObj.Save()
                PSLF.RunEpcl(pertStr)
                # Update mirror
                self.mObj.getPvals()

                self.ProcessFlag = 0
                if self.model.debug:
                    # TODO: Make this output more informative
                    print(self)
                return