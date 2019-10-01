class genericPrimeMover(object):
    """Governor class for the pslf genericPrimeMover model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts, modelDict):
        #for later reference/debug if desired
        
        self.isGeneric = True
        self.mirror = mirror
        self.dydLine = parts
        self.modelDict = modelDict

        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Id = parts[4] # Is this ID or ZONE?
        self.Rlevel = parts[5]

        self.Gen = ltd.find.findGenOnBus(self.mirror, self.Busnum, self.Id) # move away? No - think it's required. 9/30/19

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
        
        self.TurbineType = modelDict['TurbineType']

        # R is droop, permanent droop, steady state droop, electric droop
        # TODO: incorporate index numbers from modelDict.
        self.R  = parts[7] #listed as first thing in params list ... ie. +6
        self.Dt = 0

        if mirror.debug:
            print("\t...'genericPrimeMover' Model Created %d %s" % (self.Busnum,self.Busnam))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)