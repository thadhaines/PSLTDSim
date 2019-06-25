"""Used as a base class for initalizing BA Agents"""
class BA(object):
    """Generic Balancing Authority Agent"""
    def __init__(self,mirror, name, BAdict):

        # Object Links
        self.mirror = mirror
        self.name = name
        self.BAdict = BAdict
        self.actTime = float(BAdict['ActionTime'])

        # Current Value Dictionary
        self.cv = {
            'ACE' : 0.0,
            'ACEint' :0.0,
            'distStep' : 0,
            }

        # Link mirror Area to agent
        testArea = ltd.find.findAgent(self.mirror, 'area', BAdict['Area'])
        if testArea != None:
            self.Area = testArea
            testArea.BA = self

            # Handle setting B
            bStr = BAdict['B'].split(":")
            bType = bStr[1].strip()
            if bType.lower() == 's':
                # Scale Area Beta for B
                self.B = self.Area.beta * float(bStr[0])
            elif bType.lower() == 'p':
                # use percent of load
                self.B = self.Area.cv['P']*(float(bStr[0])/100.00)
            elif bType.lower() == 'abs':
                #use absolute entry as B
                self.B = float(bStr[0])
            else:
                # B type not recognized
                print("*** Balancing Authority Error - B type not recoginzed - using 1% of Load.")
                self.B = self.Area.cv['P']*0.01
        else:
            print("*** Balacing Authority Error - Area Not Found")
        
        # Participation Dictionary init
        self.pDict = {}

        # Create links to controlled machines
        for genStr in BAdict['CtrlGens']:
            parsed = genStr.split(":")
            idStr = parsed[0].split()
            pFactor = float(parsed[1])
            distType = parsed[2]

            # Attempt to find mirror Agent
            foundAgent = ltd.find.findAgent(self.mirror ,idStr[0], idStr[1:] )

            if foundAgent:
                if self.mirror.debug:
                    print('Found', foundAgent)
                # attach dist type to gen agent
                foundAgent.distType = distType

                # Create dictionary Based on Participation Factor
                if str(pFactor) in self.pDict:
                    # append dupe pFactor to previously made entry
                    self.pDict[str(pFactor)].append(foundAgent)
                else:
                    # Make new pFactor Dict
                    self.pDict[str(pFactor)] = [foundAgent]
            else:
                print('*** Balacing Authority Error: Target Agent %s Not Found.' % parsed[0])
        #end for

        # Calc participation factor sum
        self.pFsum = 0.0
        for pF in self.pDict:
            # multiply pFactor key by len of list and sum
            self.pFsum += float(pF)*len(self.pDict[pF])

        if self.pFsum != 1.0:
            print("*** Balacing Authority % has a total Participation Factor of %.2f"
                  % (self.name, self.pFsum))

        # Attach BA to mirror
        self.mirror.BA.append(self)
        self.mirror.BAdict[self.name] = self

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_ACE = [0.0]*self.mirror.dataPoints
        self.r_ACEint = [0.0]*self.mirror.dataPoints
        self.r_distStep = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_ACE[n] = self.cv['ACE']
        self.r_ACEint[n] = self.cv['ACEint']
        self.r_distStep[n] = self.cv['distStep']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_ACE = self.r_ACE[:N]
        self.r_ACEint = self.r_ACEint[:N]
        self.r_distStep = self.r_distStep[:N]