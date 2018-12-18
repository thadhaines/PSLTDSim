"""Classes that take lines from dydParser and create pseudo PSLF models in mirror
Pretty basic at the moment. Doesn't account for in line comments (common in WECC)
A more adaptive parser would be ideal.
"""

class genrou():
    """Generator class for the pslf gensal model parameters
    Class parameters populated by parsed line elements from a dyd line
    NOTE: There has got to be a better way to do this. Hardcoded indexes are a bad idea
    """
    def __init__(self, line):
        parts = line.split()
        partsq = line.split('"') # to handle odd names / zones
        
        self.Type = parts[0]
        self.Busnum = int(parts[1])
        self.Busnam = partsq[1].rstrip() # to remove double quotes, lagging ws
        self.Base_kV = float(partsq[2])
        self.Zone = partsq[3] # string with now quotes
        mbase = parts[9].split('=')
        self.Mbase = float(mbase[1]) # in MVA
        
        self.Tpdo  = float(parts[10])
        self.Tppdo = float(parts[11])
        self.Tpdq = float(parts[12])
        self.Tppqo = float(parts[13])
        self.H = float(parts[14]) # in sec
        self.D = float(parts[15])
        self.Ld = float(parts[16])
        self.Lq = float(parts[17])
        self.Lpd = float(parts[18])
        self.Lppd = float(parts[19]) 
        self.Ll = float(parts[20])
        self.S1 = float(parts[21])
        self.S12 = float(parts[22])
        self.Ra = float(parts[23])
        self.Rcomp = float(parts[24])
        self.Xcomp = float(parts[25])
        self.accel = float(parts[26])