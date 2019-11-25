class genericPrimeMover(object):
    """Governor class for the pslf genericPrimeMover model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts, modelDict):
        #for later reference/debug if desired
        self.isMachine = False
        self.isGeneric = True
        self.mirror = mirror
        self.dydLine = parts
        self.modelDict = modelDict

        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Id = parts[4].replace('"','') # ID - remove double quotes
        self.Rlevel = parts[5]

        # removing from init...
        self.Gen = ltd.find.findGenOnBus(self.mirror, self.Busnum, self.Id) # move away? No - think it's required. 9/30/19

        if self.Gen == None:
            print("*** Gen %s on Bus %s with ID %s not found. Can't add prime mover." %(self.Busnam, self.Busnum, self.Id))
        else:
            #if isinstance(parts[6], basestring):
            if isinstance(parts[6], str):
                #if '=' in parts[6]:
                mwInfo = parts[6].split('=')
                self.mwCap = float(mwInfo[1]) # in MW
            else:
                # No mwcap info found - should use generator MVA base
                parts.insert(6, 'MBASE MVA')
                self.dydLine = parts
                self.mwCap = self.Gen.Mbase # default PSDS behavior
        

            if self.mwCap == 0.0:
                # handle case where mwcap = 0 
                self.mwCap = self.Gen.Mbase

            self.TurbineType = modelDict['LTDTurbineType']

            # R is droop, permanent droop, steady state droop, electric droop
            if self.Type.lower() == 'hyg3':
                # account for 2 droop settings
                posR1 = parts[modelDict['Rloc']]  # Rgate
                posR2 = parts[modelDict['Rloc']+1] # R elec

                # handle case of zeros
                # assumes one of the two R is not zero
                if posR1 == 0.0:
                    self.R = posR2

                if posR2 == 0.0:
                    self.R = posR1

                
            else:
                self.R  = parts[modelDict['Rloc']] #listed as first thing in params list ... ie. +6


            if modelDict['Dloc'] == 'Not Listed':
                self.Dt = 0
            else:
                #self.Dt = parts[modelDict['Dloc']] # To include damping from dyd -> Ignored for now
                self.Dt = 0

            if mirror.debug:
                print("\t...'genericPrimeMover' Model Created %d %s ID %s" % (self.Busnum,self.Busnam, self.Id))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
