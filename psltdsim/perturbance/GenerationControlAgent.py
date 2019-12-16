class GenerationControlAgent(object):
    """
    Handle creating ramp perturbance agents for controlled gens according
    to participation factor as to mimic daily load dispatch.

    Must be stepped during sim as required calcs cannot be completed prior.
    """

    def __init__(self, mirror, name, paramD):
        self.mirror = mirror
        self.name = name
        self.paramD = paramD

        self.areaNum = paramD['Area']
        self.Area = ltd.find.findArea(mirror, self.areaNum)
        self.forcast = paramD['forcast']
        self.executedForcast = []

        self.timeScale = paramD['timeScale']
        self.rampType = paramD['rampType']
        self.startTime = paramD['startTime']

        self.ctrlGens = []

        self.dNDX = 0       # dispatch index

        if self.Area == None:
            print("*** Generation Control Agent Error: Area %d not found."
                  % self.areaNum)
        else:
            genRetCode = self.linkCtrlGens()
            if genRetCode:
                self.mirror.GenCTRL.append(self)
                print("*** Generation Control Agent for Area %d created." % self.areaNum)
            else:
                print("*** Generation Control Agent Error: Area %d generator link error."
                  % self.areaNum)

    def linkCtrlGens(self):
        """
        Cycle through ctrlGens string list, create links and participation 
        factor information in self.
        """
        for genStr in self.paramD['CtrlGens']:
            ptFactor = float(genStr.split(':')[1])
            idList = genStr.split(':')[0].split()
            if len(idList) >= 3: # ID is specified
                gen = ltd.find.findGenOnBus(self.mirror,idList[1],idList[2])
            else: # no ID specified
                gen = ltd.find.findGenOnBus(self.mirror,idList[1])

            # check returned gen
            if gen == None:
                print("*** Generation Control Agent Error: genStr '%s' error."
                  % genStr)
                return False
            else:
                self.ctrlGens.append( (gen, ptFactor) )
                
            return True

    def step(self):
        """
        determine if new dispatch perturbance must be created, if so, create
        """
        t = self.mirror.cv['t']
        if t == self.forcast[self.dNDX][0]*self.timeScale:
            self.createRamp()

    def createRamp(self):
        # check if last dispatch
        if (self.dNDX+1) == len(self.forcast):
            # all dispatches executed
            return

        entry = self.forcast[self.dNDX]
        if self.dNDX == 0:
            # assumes nothing happens to change Pe prior to self.startTime
            rampStart = entry[0]*self.timeScale+self.startTime
            rampDur = self.timeScale-self.startTime
        else:
            rampStart = entry[0]*self.timeScale
            rampDur = self.timeScale

        # collect required calculation varaibles
        perReq = self.forcast[self.dNDX+1][1]
        totAreaMW = self.Area.cv['Pe']
        t = self.mirror.cv['t']
        
        # create perturbances for each controlled gen
        for genTuple in self.ctrlGens:
                
            # check for gov (ramp Pref
            if genTuple[0].gov_model != False: #i.e has gov
                pertTar = 'Pref'
            else:
                pertTar = 'Pm'

            # calculate 'scaled' percent change value
            pertDelta = totAreaMW/genTuple[0].cv['Pe']*genTuple[1]*perReq
            pertParams = [pertTar, t, rampDur, pertDelta, self.rampType]
            newRampAgent = ltd.perturbance.RampAgent(self.mirror, genTuple[0], pertParams )
            if newRampAgent.ProcessFlag:
                self.mirror.Perturbance.append(newRampAgent)
                #print(newRampAgent)

        print("*** Generation Control Agent time %d to %d of %.2f percent changed added."
                % (rampStart, rampStart+rampDur, pertDelta))
        self.dNDX +=1
