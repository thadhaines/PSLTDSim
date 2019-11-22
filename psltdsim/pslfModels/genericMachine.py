"""Classes take lines from dydParser and create PSLF model data objects in mirror (system model)
Pretty basic at the moment. 
A more adaptive parser would be ideal, though may be unpossible 
"""

class genericMachine(object):
    """Generator class for the pslf genericMachine model parameters
    Class parameters populated by parsed line elements from a CLEAN dyd line
    NOTE: There may be a better way to do this. Hardcoded indexes feel like a bad idea
    """
    def __init__(self, mirror, parts, modelDict):
        #for later reference/debug if desired
        self.dydLine = parts

        self.isMachine = True
        self.isGeneric = True
        self.Type = parts[0]
        self.Busnum = parts[1]
        self.Busnam = parts[2]
        self.Base_kV = parts[3]
        self.Id = parts[4].replace('"','')
        self.Rlevel = parts[5]

        #if isinstance(parts[6], basestring):
        if isinstance(parts[6], str):
            #if '=' in parts[6]:
            mbase = parts[6].split('=')
            self.Mbase = float(mbase[1]) # in MVA
        else:
            parts.insert(6, 'BASE MVA')
            self.dydLine = parts
            self.Mbase = mirror.Sbase # TODO: test behavior

        self.H = parts[modelDict['Hloc']] # in sec # listed as fifth item in list was 11... i.e, add 6
        self.D = parts[modelDict['Dloc']] # listed as 6th thing in list (12th part. in dyd clean line)

        if mirror.debug:
            print("\t...'genericMachine' Model Created %d %s ID %s" % (self.Busnum,self.Busnam , self.Id) )

    def __repr__(self):
        """Display more useful data for model"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s\n" %(str(self.Busnum).zfill(3), self.Busnam)

        return(tag1+tag2)
