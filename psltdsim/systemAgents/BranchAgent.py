class BranchAgent(object):
    """Branch Agent class for LTD"""
    def __init__(self, mirror, area, newBranch):
        # mirror Reference
        self.mirror = mirror
        self.Area = area

        self.Ck = str(newBranch.Ck) # string
        self.ScanBus = int(newBranch.GetScanBusIndex()) #int

        self.TbusIndex = int(newBranch.Ito)
        self.FbusIndex = int(newBranch.Ifrom)

        # LTD references <- have to initialize after all buses are in LTD.
        self.Tbus = None
        self.Fbus = None

        #debug
        #print('branch %d id %s from bus %d' % 
        #(self.ScanBus, self.Ck, self.FbusIndex))

        # This may be unneccessary - breaks for somereason...
        #self.X = ltd.data.single2float(newBranch.Zsecx)
        #self.R = ltd.data.single2float(newBranch.Zsecr)
    
    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.Fbus.Extnum).zfill(3), self.Fbus.Busnam)
        # additional outputs
        tag3 = "%s %s" %(str(self.Tbus.Extnum).zfill(3), self.Tbus.Busnam)

        return(tag1+' From '+tag2+' to '+tag3)
    

    def createLTDlinks(self):
        """Create links to LTD system"""
        self.Tbus = ltd.find.findBus(self.mirror,
                                     col.BusDAO.FindByIndex(self.TbusIndex).Extnum)
        self.Fbus = ltd.find.findBus(self.mirror,
                                     col.BusDAO.FindByIndex(self.FbusIndex).Extnum)