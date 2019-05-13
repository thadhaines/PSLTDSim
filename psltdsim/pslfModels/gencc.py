class gencc(object):
    """Governor class for the pslf ggov1 model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts):
        #for later reference/debug if desired
        self.mirror = mirror
        self.dydLine = parts
        self.params = 27 # num params + 6 from id. Varies per model

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

        self.Gen = ltd.find.findGenOnBus(self.mirror, self.Busnum, self.Id)

        #if isinstance(parts[6], basestring):
        if isinstance(parts[6], str):
            #if '=' in parts[6]:
            mwInfo = parts[6].split('=')
            self.mwCap = float(mwInfo[1]) # in MW
        else:
            # No mwcap info found - should use generator MVA base
            parts.insert(6, 'BASE MVA')
            self.mwCap = 0.0 # TODO: Get most recent during dynamic init
        
        # Model specific parameters.
        self.Tpdo 		= parts[7]
        self.Tppdo		= parts[8]
        self.Tpqo 		= parts[9]
        self.Tppqo 		= parts[10]
        self.H 			= parts[11]
        self.D 			= parts[12]
        self.Ld 		= parts[13]
        self.Lq 		= parts[14]
        self.Lpd 		= parts[15]
        self.Lpq 		= parts[16]
        self.Lppd 		= parts[17]
        self.Lppq 		= parts[18]
        self.Ll 		= parts[19]
        self.S1 		= parts[20]
        self.S12 		= parts[21]
        self.Ra 		= parts[22]
        self.Rcomp 		= parts[23]
        self.Xcomp 		= parts[24]
        self.accel 		= parts[25]
        self.Pf 		= parts[26]
        self.Qf 		= parts[27]

        if mirror.debug:
            print("\t...'gencc' Model data collected for %d %s" % (self.Busnum,self.Busnam))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
