class ShuntControlAgent(object):
    """
    Handle paramD and linking to mirror agent,
    Collect and organize controlled shunts by status
    Create required timers

    each step:
        Check timer flags
        Act appropriately

    """

    def __init__(self, mirror, name, paramD):
        # Linking and Identification
        self.mirror = mirror
        self.name = name
        self.paramD = paramD

        # Locate Reference Agent
        tarType = paramD['RefAgentType']
        idList = paramD['RefAgentID']
        self.RefAgent = ltd.find.findAgent(mirror, tarType, idList)

        if self.RefAgent == None:
            print("*** Shunt Control Agent Error: Agent %s %s not found."
                  % (tarType, idList))
        else:
            # Lists for controled shunts
            self.OnShunts =[]
            self.OffShunts =[]
            # Find and collect Controlled Shunts
            for shuntSTR in self.paramD['CtrlShunts']:
                clnSTR = shuntSTR.strip().split(' ')
                shuntAgent = ltd.find.findAgent(self.mirror, clnSTR[0], clnSTR[1:] )
                if shuntAgent != None:
                    if shuntAgent.cv['St'] == 1:
                        self.OnShunts.append(shuntAgent)
                    else:
                        self.OffShunts.append(shuntAgent)

            # Create Set Timer
            self.SetTimer = ltd.systemAgents.TimerAgent(
                self.mirror, name+'SetTimer',self.RefAgent,
                self.paramD['SetLogic'],self.paramD['SetTime'],
                self.paramD['SetCountType'])
            # Create Reset Timer
            self.ResetTimer = ltd.systemAgents.TimerAgent(
                self.mirror, name+'ResetTimer',self.RefAgent,
                self.paramD['ResetLogic'],self.paramD['ResetTime'],
                self.paramD['ResetCountType'])
            # Create Hold Timer (if applicable)

            print("*** Shunt Control Agent %s %s  created."
                 % (tarType, idList))

    def step(self):
        """ check flags, send msg, else false """
        updateMSG = False
        NumOn = len(self.OnShunts)
        NumOff = len(self.OffShunts)

        if self.SetTimer.actFlag:
            # check for Off shunts
            if NumOff > 0:
                # turn shunt on
                self.OffShunts[0].cv['St'] = 1
                updateMSG = self.OffShunts[0].makeAMQPmsg()
                # move to On list
                self.OnShunts.append(self.OffShunts.pop(0))
                # Reset Timer
                self.SetTimer.reset()

                return updateMSG

        if self.ResetTimer.actFlag:
            # Check for On Shunts
            if NumOn > 0:
                # turn shunt off
                self.OnShunts[0].cv['St'] = 0
                updateMSG = self.OnShunts[0].makeAMQPmsg()
                # move to Off List
                self.OffShunts.append(self.OnShunts.pop(0))
                # Reset Timer
                self.ResetTimer.reset()

                return updateMSG

        return updateMSG