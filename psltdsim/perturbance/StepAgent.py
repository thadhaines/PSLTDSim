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

        self.attr = perParams[0]
        self.tStart = float(perParams[1])
        self.pertVal = float(perParams[2])

        

        if len(perParams) > 3 :
            if (self.tarType == 'gen') and (self.attr.lower() == 'st'):
                # to handle a restart value
                self.RestartVal = float(perParams[3])
                self.stepType = 'abs'
            else:
                self.stepType = perParams[3].lower()
        else:
            self.stepType = 'abs'

         # Check if linking is okay
        attrCheck = ltd.perturbance.getCurrentVal(self.mObj, self.attr)
        if attrCheck == None:
            # Attribute not found or other linking error
            self.ProcessFlag = 0

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))
        
        if self.tarType == 'mirror':
            # additional outputs
            tag2 = "Stepping %s of system %s at time %.2f to %.2f %s" %(
                self.attr,
                self.tarType,
                self.tStart,
                self.pertVal,
                self.stepType,
                )

        else:
            # additional outputs
            tag2 = "Stepping %s %s %s on Bus %d at time %.2f to %.2f %s" %(
                self.tarType,
                self.mObj.Id,
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
            if self.mirror.cv['t'] < self.tStart:
                # acts as a pass
                return 0

            if self.mirror.cv['t'] >= self.tStart:
                # Perform Perturbance step

                # Update correct attribute 
                if (self.attr == 'St') and (self.tarType == 'load'):
                    if (self.pertVal == 1) and (self.mObj.cv['St'] ==0):
                        self.mObj.cv['St'] = 1
                        self.mirror.ss_Pert_Pdelta += self.mObj.cv['P']
                        self.mirror.ss_Pert_Qdelta += self.mObj.cv['Q']
                    elif (self.pertVal == 0) and (self.mObj.cv['St'] ==1):
                        self.mObj.cv['St'] = 0
                        self.mirror.ss_Pert_Pdelta -= self.mObj.cv['P']
                        self.mirror.ss_Pert_Qdelta -= self.mObj.cv['Q']
                    else:
                        print("*** Perturbance Error: Status aready %d."
                              % self.pertVal)

                if (self.attr == 'St') and (self.tarType == 'gen'):
                    # Generators must adjust system inertia - 
                    # System Pm is calculated after perturbance steps
                    if (self.pertVal == 1) and (self.mObj.cv['St'] ==0):
                        self.mObj.cv['St'] = 1
                        self.mObj.cv['IRPflag'] = True
                        self.mObj.cv['Pm'] = self.RestartVal
                        self.mObj.cv['Pe'] = self.RestartVal
                        self.mObj.cv['Qmin'] = self.mObj.Qmin0
                        self.mObj.cv['Qmax'] = self.mObj.Qmax0
                        # self.mirror.flatStart = 1
                        # handle initial pm values....
                        # add inertial to system
                        #self.mirror.ss_H += self.mObj.H
                        self.mirror.cv['Hsys'] += self.mObj.H

                    elif (self.pertVal == 0) and (self.mObj.cv['St'] == 1):
                        self.mObj.cv['St'] = 0
                        self.mObj.cv['IRPflag'] = False
                        #if self.mirror.debug: print('setting flat start')
                        #self.mirror.flatStart = 1
                        self.mObj.cv['Pm'] = 0
                        self.mObj.cv['Pe'] = 0
                        self.mObj.cv['Qmin'] = 0
                        self.mObj.cv['Qmax'] = 0
                        #remove inertia from system
                        #self.mirror.ss_H -= self.mObj.H
                        self.mirror.cv['Hsys'] -= self.mObj.H
                    else:
                        print("*** Perturbance Error: Status aready %d."
                              % self.pertVal)
                    #TODO: handle different actions for certain agent types.

                elif self.attr == 'P':
                    oldVal = self.mObj.cv['P']
                    if self.stepType == 'rel':
                        self.mObj.cv['P'] += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.cv['P'] = self.mObj.cv['P'] * (1+self.pertVal/100.00) # percent change
                    else:
                        self.mObj.cv['P'] = self.pertVal # absolute step

                    self.mirror.ss_Pert_Pdelta += self.mObj.cv['P'] - oldVal

                elif self.attr.lower() == 'Q':
                    oldVal = self.mObj.cv['Q']
                    if self.stepType == 'rel':
                        self.mObj.cv['Q'] += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.cv['Q'] = self.mObj.cv['Q'] * (1+self.pertVal/100.00) # percent change
                    else:
                        self.mObj.cv['Q'] = self.pertVal # absolute step

                    self.mirror.ss_Pert_Qdelta += self.mObj.cv['Q'] - oldVal


                # Generic way to handle current value steps.
                elif self.attr in self.mObj.cv:
                    # Used to change any attribute in current value dictionary

                    oldVal = self.mObj.cv[self.attr]
                    if self.stepType == 'rel':
                        self.mObj.cv[self.attr] += self.pertVal # relative step
                    elif self.stepType == 'per':
                        self.mObj.cv[self.attr] = self.mObj.cv[self.attr] * (1+self.pertVal/100.00)
                    else:
                        self.mObj.cv[self.attr] = self.pertVal # absolute step

                    # Handle setting states if governed machine PM is stepped.
                    # i.e. used to simulate dropping generation in controlled plant
                    if self.attr == 'Pm' and hasattr(self.mObj, 'gov_model'):
                        # Stepping mechanical power on generator
                        if self.mObj.gov_model != False:
                            # states must be adjusted  on 
                            self.mObj.gov_model.setState(self.mObj.cv[self.attr])

                self.ProcessFlag = 0
                if self.mirror.debug:
                    # TODO: Make this output more informative
                    print(self)

                return 1