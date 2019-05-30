class StepAgent(object):
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
                return 0

            if self.mirror.c_t >= self.tStart:
                # Perform Perturbance step

                # Update correct attribute 
                if self.attr.lower() == 'st':
                    #TODO: handle different actions for each agent type...
                    if self.pertVal == 1:
                        mObj.St = 1
                        self.mirror.ss_Pert_Pdelta += mObj.P
                        self.mirror.ss_Pert_Qdelta += mObj.Q
                    else:
                        mObj.St = 0
                        self.mirror.ss_Pert_Pdelta -= mObj.P
                        self.mirror.ss_Pert_Qdelta -= mObj.Q

                elif self.attr.lower() == 'p':
                    oldVal = self.mObj.P
                    if self.stepType.lower() == 'rel':
                        self.mObj.P += self.pertVal # relative step
                    else:
                        self.mObj.P = self.pertVal # absolute step

                    self.mirror.ss_Pert_Pdelta += self.mObj.P - oldVal

                elif self.attr.lower() == 'q':
                    oldVal = self.mObj.Q
                    self.mObj.Q = self.pertVal
                    mirror.ss_Pert_Qdelta += self.pertVal - oldVal

                elif self.attr.lower() == 'pset':
                    oldVal = self.mObj.Pset
                    if self.stepType.lower() == 'rel':
                        self.mObj.Pset += self.pertVal # relative step
                    else:
                        self.mObj.Pset = self.pertVal # absolute step

                self.ProcessFlag = 0
                if self.mirror.debug:
                    # TODO: Make this output more informative
                    print(self)
                return 1