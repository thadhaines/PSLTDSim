class RTAgent(object):
    """ Reference/Target Agent
    to be used to clarify creating and validating agents used in DTC
    also to functionalize getting and setting values
    """

    def __init__(self,mirror, DTCAgent, name, inputSTR):
        self.mirror = mirror
        self.DTCAgent = DTCAgent
        self.inputSTR = inputSTR

        self.idList = inputSTR.split(':')[0].strip().split(' ')
        self.attr = inputSTR.split(':')[1].strip()
        self.rtOK = True
        self.rtAgent = None

        newRT = ltd.find.findAgent(mirror, self.idList[0], self.idList[1:])
        if newRT == None:
            print("*** RT Error: Agent not found %s " % inputSTR)
            self.rtOK = False

        # confirm Attribute
        if self.attr not in newRT.cv:
            print("*** RT Error: didn't find attribute... %s " % inputSTR)
            self.rtOK = False

        # If found agent has correct attribute, store reference
        if self.rtOK:
            self.rtAgent = newRT

    def getNewAttr(self):
        """Return most recent rtAttribute"""
        return self.rtAgent.cv[self.attr]

    def getNewAttrSTR(self):
        """Return most recent rtAttribute as a string"""
        return str(self.rtAgent.cv[self.attr])

    def setNewAttr(self, operation, newVAl):
        """Set attribute to newVal via operation
        returns AMQP update message"""
        exec('self.rtAgent.cv[self.attr]'+ operation + str(newVAl))
        return self.rtAgent.makeAMQPmsg()