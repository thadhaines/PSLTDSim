class LoadStepAgent(object):
    """Performs steps of P, Q, or St on Loads - calculates Perturbance deltas
    targetObj is a python mirror agent object reference
    perParams is a list: [targetAttr, tStart, pertVal]
    Updated to NOT save any PSLF objects attached to self.
    """

    def __init__(self, mirror, targetObj, perParams):
        self.ProcessFlag = 1

        self.mirror = mirror
        self.mObj = targetObj

        self.attr = perParams[0]
        self.tStart = float(perParams[1])
        self.pertVal = float(perParams[2])

        if len(perParams) > 3 :
            self.stepType = perParams[3]
        else:
            self.stepType = 'abs'

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Stepping %s on Bus %d at time %.2f to %.2f %s" %(
            self.attr,
            self.mObj.Bus.Extnum,
            self.tStart,
            self.pertVal,
            self.stepType,
            )

        return(tag1+tag2)

    def step(self):
        """Function called every timestep - takes action only once"""
        if self.ProcessFlag:
            if self.mirror.c_t < self.tStart:
                # acts as a pass
                return

            if self.mirror.c_t >= self.tStart:
                # Perform Perturbance step
                # Get most recent PSLF reference
                pObj = self.mObj.getPref()
                
                # Update correct attribute in PSLF
                if self.attr.lower() == 'st':
                    if self.pertVal == 1:
                        pObj.SetInService()
                        self.mirror.ss_Pert_Pdelta += pObj.P
                        self.mirror.ss_Pert_Qdelta += pObj.Q
                    else:
                        pObj.SetOutOfService()
                        self.mirror.ss_Pert_Pdelta -= pObj.P
                        self.mirror.ss_Pert_Qdelta -= pObj.Q

                elif self.attr.lower() == 'p':
                    oldVal = pObj.P
                    if self.stepType.lower() == 'rel':
                        pObj.P += self.pertVal # relative step
                    else:
                        pObj.P = self.pertVal # absolute step

                    self.mirror.ss_Pert_Pdelta += pObj.P - oldVal

                elif self.attr.lower() == 'q':
                    oldVal = pObj.Q
                    pObj.Q = self.pertVal
                    mirror.ss_Pert_Qdelta += self.pertVal - oldVal

                # Save Changes in PSLF
                pObj.Save()
                # Update mirror
                self.mObj.getPvals()

                self.ProcessFlag = 0
                if self.mirror.debug:
                    # TODO: Make this output more informative
                    print(self)
                return