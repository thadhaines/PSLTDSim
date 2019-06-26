class PowerPlantAgent(object):
    """Collection of Agents to further distribute ACE to"""
    def __init__(self,mirror,name, genList):

        self.__class__ = PowerPlantAgent
        # Input references
        self.mirror = mirror
        self.name = name
        self.genList = genList
        self.distType = None # Used for BA distribution
        #Keep track of distributed ACE per unit?... Gen -> recACE?

        # Participation Dictionary init
        self.pDict = {}

        # Find Agents in Generator list
        for genStr in genList:
            parsed = genStr.split(":")
            idStr = parsed[0].split()
            pFactor = float(parsed[1])
            distType = parsed[2].strip()
            # Attempt to find mirror Agent
            foundAgent = ltd.find.findAgent(self.mirror ,idStr[0], idStr[1:] )

            if foundAgent:
                if self.mirror.debug:
                    print('Found', foundAgent)
                agentRef = foundAgent
                foundAgent.distType = distType
                # Create dictionary Based on Participation Factor
                if str(pFactor) in self.pDict:
                    # append dupe pFactor to previously made entry
                    self.pDict[str(pFactor)].append(foundAgent)
                else:
                    # Make new pFactor Dict
                    self.pDict[str(pFactor)] = [foundAgent]
            else:
                print('*** Power Plant Error: Target Agent %s Not Found.' % parsed[0])
        #end for
        # Calc participation factor sum
        self.pFsum = 0.0
        for pF in self.pDict:
            # multiply pFactor key by len of list and sum
            self.pFsum += float(pF)*len(self.pDict[pF])

        if self.pFsum != 1.0:
            print("*** Power Plant % has a total Participation Factor of %.2f"
                  % (self.name, self.pFsum))
        # Attach PowerPlant to Mirror
        self.mirror.PowerPlant.append(self)
        self.mirror.ppDict[self.name] = self