class LoadControlAgent(object):
    """
    Handle creating ramp perturbance agents for all area loads to mimic
    daily load changes.
    Only acts on laods that are on during initialization.
    """

    def __init__(self, mirror, name, paramD):
        self.mirror = mirror
        self.name = name
        self.paramD = paramD

        self.areaNum = paramD['Area']
        self.Area = ltd.find.findArea(mirror, self.areaNum)
        self.demand = paramD['demand']
        self.timeScale = paramD['timeScale']
        self.rampType = paramD['rampType']
        self.startTime = paramD['startTime']

        if self.Area == None:
            print("*** Load Control Agent Error: Area %d not found."
                  % self.areaNum)
        else:
            self.createRamps()
            print("*** Load Control Agent for Area %d created." % self.areaNum)


    def createRamps(self):
        # get perturbance data from inputs
        firstEntry = True
        for entry in self.demand:
            rampDur = self.timeScale
            if firstEntry:
                prevTime = entry[0]*self.timeScale+self.startTime
                rampDur = self.timeScale-self.startTime # handle ramp offset
                firstEntry = False
                continue
            curTime = entry[0]*self.timeScale
            pertDelta = entry[1]
            
            # create perturbances for each load
            for load in self.Area.Load:
                pertParams = ['P', prevTime, rampDur, pertDelta, self.rampType]
                newRampAgent = ltd.perturbance.RampAgent(self.mirror, load, pertParams )
                if newRampAgent.ProcessFlag and (load.cv['St'] ==1):
                    self.mirror.Perturbance.append(newRampAgent)
                    #print(newRampAgent)

            print("*** Load Control Agent time %d to %d of %.2f percent changed added."
                  % (prevTime, curTime, pertDelta))
            prevTime = curTime
