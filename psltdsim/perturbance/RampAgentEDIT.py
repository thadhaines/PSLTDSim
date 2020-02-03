class RampAgentEDIT(object):
    """ Removal of second ramp - may or may not use in the future....
    Performs absolute, percent change, and relative ramps of:
    P or Q on Loads (calculates Perturbance deltas for system mirror)
    Pset on Governed machines 
    Pm for non governed machines
    targetObj is a python mirror agent object reference
    perParams is a list: 
    [targetAttr, tStart, RAtime, RAVal, RAtype holdTime, RBtime, RBVal RBtype]
    """

    def __init__(self, mirror, targetObj, perParams):
        self.ProcessFlag = 1

        self.mirror = mirror
        self.mObj = targetObj

        """ #removing second ramp
        # Handle under defined cases
        if len(perParams) < 5:
            perParams.append('rel')
        if len(perParams) < 6:
            short = 9-len(perParams)
            for x in range(short):
                perParams.append(0.0)
            perParams[8] = 'none'
        if len(perParams) < 9:
            perParams.append('rel')
        """

        self.attr = perParams[0]

        # Check if linking is okay
        attrCheck = ltd.perturbance.getCurrentVal(self.mObj, self.attr)
        if not attrCheck:
            # Attribute not found or other linking error
            self.ProcessFlag = 0

        self.startTime = float(perParams[1])
        self.RAtime = float(perParams[2])
        self.RAVal = float(perParams[3])
        self.RAtype = perParams[4].lower()


        # calculate relative ramp slope increment based of rel ramp type
        if self.RAtype == 'rel':
            self.RAslope = self.RAVal/self.RAtime*mirror.timeStep
        else:
            self.RAslope = None # must calculate absolute and % change base off current sim values

        self.endTime = self.startTime+self.RAtime # +self.holdTime+self.RBtime

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs

        tag2 = "Ramping %s on Bus %d ID %s at time %.2f by %.2f %s" %(
            self.attr,
            self.mObj.Bus.Extnum,
            self.mObj.Id,
            self.startTime,
            self.RAVal,
            self.RAtype,
            )


        return(tag1+tag2)

    def step(self):
        """Function called every timestep"""
        if self.ProcessFlag:
            if self.mirror.cv['t'] < self.startTime:
                # acts as a `wait until action'
                return 0

            if self.mirror.cv['t'] > self.startTime:
                if self.mirror.cv['t'] > self.endTime:
                    # turn off action
                    self.ProcessFlag = 0
                    return 0
                
                self.increment = 0
                # Select correct ramp incremenct
                if self.mirror.cv['t'] <= (self.startTime + self.RAtime):
                    # process ramp A

                    # calculate increments for percent and absolute if not calculated yet
                    if not self.RAslope:
                        curVal = ltd.perturbance.getCurrentVal(self.mObj, self.attr)
                        # calculate perent change
                        if self.RAtype == 'per':
                            newVal = curVal*(1+self.RAVal/100.00)
                            self.RAslope = (newVal-curVal)/self.RAtime*self.mirror.timeStep
                        # calculate absolute change slope
                        if self.RAtype == 'abs':
                            self.RAslope = (self.RAVal - curVal)/self.RAtime*self.mirror.timeStep

                    self.increment = self.RAslope

                # Update correct attribute 
                if self.attr.lower() == 'p':
                    oldVal = self.mObj.cv['P']
                    self.mObj.cv['P'] += self.increment
                    self.mirror.ss_Pert_Pdelta += self.increment

                elif self.attr.lower() == 'q':
                    oldVal = self.mObj.cv['Q']
                    self.mObj.cv['Q'] += self.increment
                    mirror.ss_Pert_Qdelta += self.increment

                elif self.attr in self.mObj.cv:
                    # Used to handle Pref, and Pm... in a general way
                    oldVal = self.mObj.cv[self.attr]
                    self.mObj.cv[self.attr] += self.increment

                if self.mirror.debug:
                    # TODO: Make this output more informative or remove?
                    print(self)
                return 1