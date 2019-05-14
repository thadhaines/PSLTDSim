class ggov1(object):
    """Governor class for the pslf ggov1 model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts):
        #for later reference/debug if desired
        self.mirror = mirror
        self.dydLine = parts
        self.params = 41 # num params + 6 from id. Varies per model

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
        self.r = parts[7]
        self.rselect = parts[8]
        self.Tpelec = parts[9]
        self.maxerr = parts[10]
        self.minerr = parts[11]
        self.Kpgov = parts[12]
        self.Kigov = parts[13]
        self.Kdgov = parts[14]
        self.Tdgov = parts[15]
        self.vmax = parts[16]
        self.vmin = parts[17]
        self.Tact = parts[18]
        self.Kturb = parts[19]
        self.wfnl = parts[20]
        self.Tb = parts[21]
        self.Tc = parts[22]
        self.Flag = parts[23]
        self.Teng = parts[24]
        self.Tfload = parts[25]
        self.Kpload = parts[26]
        self.Kiload = parts[27]
        self.Ldref = parts[28]
        self.Dm = parts[29]
        self.ropen = parts[30]
        self.rclose = parts[31]
        self.Kimw = parts[32]
        self.Pmwset = parts[33]
        self.aset = parts[34]
        self.Ka = parts[35]
        self.Ta = parts[36]
        self.db = parts[37]
        self.Tsa = parts[38]
        self.Tsb = parts[39]
        self.rup = parts[40]
        self.rdown = parts[41]

        if mirror.debug:
            print("\t...'ggov1' Model data collected for %d %s" % (self.Busnum,self.Busnam))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
