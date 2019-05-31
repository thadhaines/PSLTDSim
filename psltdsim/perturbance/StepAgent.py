class StepAgent(object):
    """Performs steps of parameters in targetObj (mirror agent object reference)
    perParams is a list: [targetAttr, tStart, pertVal, pertType]
    If perType is empy - assumed to be absolute change
    Loads can step: P, Q, or St (Perturbance deltas are caluclated)
    """

    def __init__(self, mirror, targetObj, tarType, perParams):
        self.ProcessFlag = 1

        self.mirror = mirror
        self.tarType = tarType.lower()
        self.mObj = targetObj

        self.attr = perParams[0].lower()
        self.tStart = float(perParams[1])
        self.pertVal = float(perParams[2])

        if len(perParams) > 3 :
            self.stepType = perParams[3].lower()
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
                if self.attr == 'st':
                    if self.tarType == 'load':
                        if self.pertVal == 1:
                            mObj.St = 1
                            self.mirror.ss_Pert_Pdelta += mObj.P
                            self.mirror.ss_Pert_Qdelta += mObj.Q
                        else:
                            mObj.St = 0
                            self.mirror.ss_Pert_Pdelta -= mObj.P
                            self.mirror.ss_Pert_Qdelta -= mObj.Q
                    #TODO: handle different actions for each agent type...

                elif self.attr == 'p':
                    oldVal = self.mObj.P
                    if self.stepType == 'rel':
                        self.mObj.P += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.P = self.mObj.P * (1+self.pertVal/100.00) # percent change
                    else:
                        self.mObj.P = self.pertVal # absolute step

                    self.mirror.ss_Pert_Pdelta += self.mObj.P - oldVal

                elif self.attr.lower() == 'q':
                    oldVal = self.mObj.Q
                    if self.stepType == 'rel':
                        self.mObj.Q += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.Q = self.mObj.Q * (1+self.pertVal/100.00) # percent change
                    else:
                        self.mObj.Q = self.pertVal # absolute step

                    self.mirror.ss_Pert_Qdelta += self.mObj.Q - oldVal

                elif self.attr == 'pset':
                    # Used to change Pref of governed machine
                    oldVal = self.mObj.Pset
                    if self.stepType == 'rel':
                        self.mObj.Pset += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.Pset = self.mObj.Pset * (1+self.pertVal/100.00)
                    else:
                        self.mObj.Pset = self.pertVal # absolute step

                elif self.attr.lower() == 'pm':
                    # Used to change Mechanical power of non gov machine.
                    oldVal = self.mObj.Pm
                    if self.stepType == 'rel':
                        self.mObj.Pm += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.Pm = self.mObj.Pm * (1+self.pertVal/100.00)
                    else:
                        self.mObj.Pm = self.pertVal # absolute step

                self.ProcessFlag = 0
                if self.mirror.debug:
                    # TODO: Make this output more informative
                    print(self)
                return 1