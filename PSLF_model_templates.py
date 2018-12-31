"""Classes that take lines from dydParser and create pseudo PSLF models in mirror
Pretty basic at the moment. Doesn't account for in line comments (common in WECC)
A more adaptive parser would be ideal.
"""

class genrou():
    """Generator class for the pslf gensal model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There has got to be a better way to do this. Hardcoded indexes are a bad idea
    """
    def __init__(self, parts, m_ref):
        #for later reference if desired
        self.dydLine = parts

        #for underdefined models, add zeros, length specific to model type
        if len(parts)<25:
            short = 25-len(parts)
            for x in range(short):
                parts.append(0.0)

        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Zone = parts[4]
        self.Rlevel = parts[5]

        if isinstance(parts[6], basestring):
            #if '=' in parts[6]:
            mbase = parts[6].split('=')
            self.Mbase = float(mbase[1]) # in MVA
        else:
            parts.insert(6, 'BASE MVA')
            self.Mbase = m_ref.Sbase # TODO: test behavior
        
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
        self.Accel = parts[24] # not in genrou model, included in WECC

        if m_ref.debug:
            print("'genrou' Model Created %d %s" % (self.Busnum,self.Busnam))