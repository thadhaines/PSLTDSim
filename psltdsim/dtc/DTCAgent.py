class DTCAgent(object):
    """
    Definite Time Controller
    Similar to shunt controller
    handles multiple references,tarfs, enables easier user input of logic
    Assumes set, reset and hold timers
    """

    def __init__(self, mirror, name, paramD):
        self.mirror = mirror
        self.name = name
        self.paramD = paramD
        self.ra ={} # blank dictionary for references
        self.tar = {} # blank dictionary for targets
        self.Timer = {}

        # find and validate all reference Agents
        for ra in self.paramD['RefAgents']:
            inputSTR = self.paramD['RefAgents'][ra]
            newRA = ltd.dtc.RTAgent(mirror, self, ra, inputSTR)
            if newRA.rtOK:
                # add to ref agent dictionary
                self.ra[ra] = newRA

        # find and validate all reference Agents
        for tar in self.paramD['TarAgents']:
            inputSTR = self.paramD['TarAgents'][tar]
            
            newTar = ltd.dtc.RTAgent(mirror, self, tar, inputSTR)
            if newTar.rtOK:
                # add to tar agent dictionary
                self.tar[tar] = newTar

        # Create Set Timer
        self.SetTimer = ltd.dtc.DTCTimerAgent(
            self.mirror, self,  name+'SetTimer',
            self.paramD['Timers']['set'],)
        
        self.ResetTimer = ltd.dtc.DTCTimerAgent(
            self.mirror, self,  name+'ResetTimer',
            self.paramD['Timers']['reset'],)

        # Create Hold Timer (if applicable) #notice alt timer...
        if self.paramD['Timers']['hold'] > 0:
            self.HoldTimer = ltd.systemAgents.TimerAgent(
                self.mirror, name+'HoldTimer', self.mirror,
                'f : >0',self.paramD['Timers']['hold'])
        else:
            self.HoldTimer = None

        print("*** Definite Time Controller: %s created."
                % (name))

    def resetTimers(self):
        """ reset timers, handle optional hold timer """
        self.SetTimer.reset()
        self.ResetTimer.reset()
        if self.HoldTimer is not None:
            self.HoldTimer.reset()

    def getAnyOFFTar(self):
        """ return reerence to any OFF target reference"""
        # remove any previous anyOFFTar
        if 'anyOFFTar' in self.tar:
            del self.tar['anyOFFTar']

        for tarKey in self.tar:
            if self.tar[tarKey].rtAgent.cv['St'] == 0:
                return self.tar[tarKey]
        return None

    def getAnyONTar(self):
        """ return reerence to any ON target reference"""
        # remove any previous anyONTar
        if 'anyONTar' in self.tar:
            del self.tar['anyONTar']

        for tarKey in self.tar:
            if self.tar[tarKey].rtAgent.cv['St'] == 1:
                return self.tar[tarKey]
        return None

    def step(self):
        """ check flags, send msg, else false """
        updateMSG = False

        # check for hold timer
        if self.HoldTimer is not None:
            # if still holding, 'pass'
            if self.HoldTimer.actFlag == False:
                return updateMSG

        # Account for variable targetting / acting...
        self.tar['anyOFFTar'] = self.getAnyOFFTar()
        self.tar['anyONTar'] = self.getAnyONTar()

        if self.SetTimer.actFlag:
            # parse action string
            actParse = self.SetTimer.timerD['act'].split(' ')
            # acquire target agent
            if actParse[0] in self.tar:
                if type(self.tar[actParse[0]]) != type(None):
                    TA = self.tar[actParse[0]]
                    updateMSG = TA.setNewAttr(actParse[1] , actParse[2])
                    # Reset Timers
                    self.resetTimers()
                    return updateMSG

        if self.ResetTimer.actFlag:
            # parse action string
            actParse = self.ResetTimer.timerD['act'].split(' ')
            # acquire target agent
            if actParse[0] in self.tar:
                if type(self.tar[actParse[0]]) != type(None):
                    TA = self.tar[actParse[0]]
                    updateMSG = TA.setNewAttr(actParse[1] , actParse[2])
                    # Reset Timers
                    self.resetTimers()
                    return updateMSG

        return updateMSG
