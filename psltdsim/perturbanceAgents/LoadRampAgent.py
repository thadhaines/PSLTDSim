class LoadRampAgent(object):
    """Performs ramps of P (maybe Q) on Loads - calculates Perturbance deltas
    targetObj is a python mirror agent object reference
    perParams is a list: 
    [targetAttr, tStart, RAtime, RAVal, holdTime, RBtime, RBVal]
    Updated to NOT save any PSLF objects attached to self.
    """

    def __init__(self, mirror, targetObj, perParams):
        self.ProcessFlag = 1

        self.mirror = mirror
        self.mObj = targetObj

        self.attr = perParams[0]
        self.startTime = float(perParams[1])
        self.RAtime = float(perParams[2])
        self.RAVal = float(perParams[3])
        self.holdTime= float(perParams[4])
        self.RBtime= float(perParams[5])
        self.RBVal= float(perParams[6])

        self.RAslope = self.RAVal/self.RAtime*mirror.timeStep
        self.RBslope = self.RBVal/self.RBtime*mirror.timeStep

        self.endTime = self.startTime+self.RAtime+self.holdTime+self.RBtime

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Ramping %s on Bus %d at time %.2f by %.2f then by %.2f at %.2f" %(
            self.attr,
            self.mObj.Bus.Extnum,
            self.startTime,
            self.RAVal,
            self.RBVal,
            self.startTime+self.RAtime+self.holdTime,
            )

        return(tag1+tag2)

    def step(self):
        """Function called every timestep - takes action only once"""
        if self.ProcessFlag:
            if self.mirror.c_t < self.startTime:
                # acts as a pass
                return 0

            if self.mirror.c_t > self.startTime:
                if self.mirror.c_t > self.endTime:
                    self.ProcessFlag = 0
                    return 0

                # Select correct ramp incremenct
                if self.mirror.c_t <= (self.startTime + self.RAtime):
                    increment = self.RAslope
                elif self.mirror.c_t > (self.startTime + self.RAtime + self.holdTime):
                    increment = self.RBslope
                else:
                    increment = 0

                # Update correct attribute 
                if self.attr.lower() == 'p':
                    oldVal = self.mObj.P
                    self.mObj.P += increment
                    self.mirror.ss_Pert_Pdelta += increment #self.mObj.P - oldVal

                elif self.attr.lower() == 'q':
                    oldVal = self.mObj.Q
                    self.mObj.Q += increment
                    mirror.ss_Pert_Qdelta += increment #self.pertVal - oldVal

                if self.mirror.debug:
                    # TODO: Make this output more informative
                    print(self)
                return 1