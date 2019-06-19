"""Classes take lines from dydParser and create PSLF model data objects in mirror (model)
Pretty basic at the moment. 
A more adaptive parser would be ideal, though may be unpossible 
"""

class genrou(object):
    """Generator class for the pslf gensal model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, model, parts):
        #for later reference/debug if desired
        self.dydLine = parts

        #for underdefined models, add zeros
        # NOTE: length specific to model type
        if len(parts)<25:
            short = 25-len(parts)
            for x in range(short):
                parts.append(0.0)

        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Id = parts[4]
        self.Rlevel = parts[5]

        #if isinstance(parts[6], basestring):
        if isinstance(parts[6], str):
            #if '=' in parts[6]:
            mbase = parts[6].split('=')
            self.Mbase = float(mbase[1]) # in MVA
        else:
            parts.insert(6, 'BASE MVA')
            self.Mbase = model.Sbase # TODO: test behavior
        
        self.Tpdo  = parts[7]
        self.Tppdo = parts[8]
        self.Tpdq = parts[9]
        self.Tppqo = parts[10]
        self.H = parts[11] # in sec
        self.D = parts[12]
        self.Ld = parts[13]
        self.Lq = parts[14]
        self.Lpd = parts[15]
        self.Lpq = parts[16]
        self.Lppd = parts[17] 
        self.Ll = parts[18]
        self.S1 = parts[19]
        self.S12 = parts[20]
        self.Ra = parts[21]
        self.Rcomp = parts[22]
        self.Xcomp = parts[23]
        self.Accel = parts[24] # not described in available PSLF manual genrou model, included in WECC

        if model.debug:
            print("\t...'genrou' Model Created %d %s" % (self.Busnum,self.Busnam))

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
