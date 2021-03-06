class tgov1(object):
    """Governor class for the pslf tgov1 model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts):
        #for later reference/debug if desired
        self.isGeneric = False
        self.mirror = mirror
        self.dydLine = parts
        self.params = 13    # NOTE: length specific to model type

        #for underdefined models, add zeros
        if len(parts)<self.params:
            short = self.params-len(parts)
            for x in range(short):
                parts.append(0.0)

        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Id = parts[4] # Is this ID or ZONE?
        self.Rlevel = parts[5]

        self.Gen = ltd.find.findGenOnBus(self.mirror, self.Busnum, self.Id) # move away?

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
                self.mwCap = self.Gen.Mbase # default PSDS behavior
        
            self.R  = parts[7]
            self.T1 = parts[8]
            self.Vmax = parts[9]
            self.Vmin = parts[10]
            self.T2 = parts[11] # in sec
            self.T3 = parts[12]
            self.Dt = parts[13]

            if mirror.debug:
                print("\t...'tgov' Model Created %d %s" % (self.Busnum,self.Busnam))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
