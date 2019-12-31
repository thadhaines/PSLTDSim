"""Used as a base class for initalizing BA Agents"""
class BA(object):
    """Generic Balancing Authority Agent"""
    def __init__(self,mirror, name, BAdict):

        # Object Links
        self.mirror = mirror
        self.name = name
        self.BAdict = BAdict
        self.actTime = float(BAdict['AGCActionTime'])

        # Handle optional agc ramp time param
        if hasattr(BAdict, 'AGCRampTime'):
            self.rampTime = float(BAdict['AGCRampTime'])
        else:
            self.rampTime = float(BAdict['AGCActionTime'])

        self.ctrlMachines = []

        # Current Value Dictionary
        self.cv = {
            'RACE' : 0.0, # reported
            'IACE' :0.0, # integral
            'ACEFB' :0.0, # frequency bias
            'ACETL' :0.0, # tie-line bias
            'SACE' :0.0, # smoothed
            'condACE' :0.0, # conditional
            'ACE2dist' : 0.0,
            'distStep' : 0,
            }

        # Link mirror Area to agent
        testArea = ltd.find.findAgent(self.mirror, 'area', BAdict['Area'])
        if testArea != None:
            self.Area = testArea
            testArea.BA = self

            # Handle setting frequency Bias B
            bStr = BAdict['B'].split(":")
            bType = bStr[1].strip()
            if bType.lower() == 'scalebeta':
                # Scale Area Beta for B
                self.B = self.Area.beta * float(bStr[0])
            elif bType.lower() == 'perload':
                # use percent of load
                self.B = self.Area.cv['P']*(float(bStr[0])/100.00)
            elif bType.lower() == 'permax':
                # use percent of max capacity
                self.B = self.Area.MaxCapacity*(float(bStr[0])/100.00)
            elif bType.lower() == 'abs':
                #use absolute entry as B
                self.B = float(bStr[0])
            else:
                # B type not recognized
                print("*** Balancing Authority Error - B type not recoginzed - using 1% of Current Load.")
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

            # Attempt to find mirror Agent
            foundAgent = ltd.find.findAgent(self.mirror ,idStr[0], idStr[1:] )

            if foundAgent:
                if self.mirror.debug:
                    print('Found', foundAgent)

                # Create dictionary Based on Participation Factor
                if str(pFactor) in self.pDict:
                    # append dupe pFactor to previously made entry
                    self.pDict[str(pFactor)].append(foundAgent)
                else:
                    # Make new pFactor Dict
                    self.pDict[str(pFactor)] = [foundAgent]

                # Add generators to BA ctrlMachines list
                # check if power plant
                if isinstance(foundAgent, ltd.systemAgents.PowerPlantAgent):
                    # for each % entry in the PP pDict
                    for key in foundAgent.pDict:
                        # for each gen in participation group
                        for PPgen in foundAgent.pDict[key]:
                            self.ctrlMachines.append(PPgen)
                            if PPgen.ACEpFactor == None:
                                PPgen.ACEpFactor = float(pFactor)*float(key)
                            else:
                                print("*** Balanacing Authority Error: Duplicate Entry %s" % PPgen)
                else:
                    # Found Agent Not a power plant
                    # attach dist type to gen agent
                    distType = parsed[2].strip()
                    foundAgent.distType = distType
                    self.ctrlMachines.append(foundAgent)
                    if foundAgent.ACEpFactor == None:
                                foundAgent.ACEpFactor = float(pFactor)
                    else:
                        print("*** Balanacing Authority Error: Duplicate Entry %s" % foundAgent)

            else:
                print('*** Balacing Authority Error: Target Agent %s Not Found.' % parsed[0])
        #end for

        # Calc participation factor (pF) sum
        self.pFsum = 0.0

        for gen in self.ctrlMachines:
            self.pFsum += gen.ACEpFactor

        if self.pFsum != 1.0:
            print("*** Balacing Authority %s has a total Participation Factor of %.2f"
                  % (self.name, self.pFsum))

        # NOTE: Duplicate machines note checked.

        # Handle filter settings
        if self.BAdict['ACEFiltering'] != None:

            filterInput = self.BAdict['ACEFiltering'].split(":")

            if filterInput[0].lower().strip() == 'lowpass':
                T1 = float(filterInput[1])
                self.filter = ltd.filterAgents.lowPassAgent(self.mirror,self,T1)
            elif filterInput[0].lower().strip() == 'integrator':
                k = float(filterInput[1])
                self.filter = ltd.filterAgents.integratorAgent(self.mirror,self,k)
            elif filterInput[0].lower().strip() == 'pi':
                params = filterInput[1].split()
                k = float(params[0])
                a = float(params[1])
                self.filter = ltd.filterAgents.PIAgent(self.mirror,self,k,a)
        else:
            self.filter = None

        # Attach BA to mirror
        self.mirror.BA.append(self)
        self.mirror.BAdict[self.name] = self

    def initRunningVals(self):
        """Initialize history values of mirror agent"""
        self.r_RACE = [0.0]*self.mirror.dataPoints
        self.r_ACEFB = [0.0]*self.mirror.dataPoints
        self.r_ACETL = [0.0]*self.mirror.dataPoints
        self.r_SACE = [0.0]*self.mirror.dataPoints
        self.r_IACE = [0.0]*self.mirror.dataPoints
        self.r_ACE2dist = [0.0]*self.mirror.dataPoints
        self.r_distStep = [0.0]*self.mirror.dataPoints
        self.r_condACE = [0.0]*self.mirror.dataPoints

        if self.filter != None:
            self.r_SACE = [0.0]*self.mirror.dataPoints

    def logStep(self):
        """Step to record log history"""
        n = self.mirror.cv['dp']
        self.r_RACE[n] = self.cv['RACE']
        self.r_ACEFB[n] = self.cv['ACEFB']
        self.r_ACETL[n] = self.cv['ACETL']
        self.r_SACE[n] = self.cv['SACE']
        self.r_IACE[n] = self.cv['IACE']
        self.r_ACE2dist[n] = self.cv['ACE2dist']
        self.r_distStep[n] = self.cv['distStep']
        self.r_condACE[n] = self.cv['condACE']

    def popUnsetData(self,N):
        """Erase data after N from non-converged cases"""
        self.r_RACE = self.r_RACE[:N]
        self.r_ACETL = self.r_ACETL[:N]
        self.r_ACEFB = self.r_ACEFB[:N]
        self.r_SACE = self.r_SACE[:N]
        self.r_IACE = self.r_IACE[:N]
        self.r_ACE2dist = self.r_ACE2dist[:N]
        self.r_distStep = self.r_distStep[:N]
        self.r_condACE = self.r_condACE[:N]