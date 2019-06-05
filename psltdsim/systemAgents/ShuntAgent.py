class ShuntAgent(object):
    """Shunt Agent for LTD mirror"""
    #NOTE : incomplete as of 5/16/19. only basic id and casting functionality.
    def __init__(self,mirror,parentBus,newShunt):

        # mirror Reference
        self.mirror = mirror
        self.Bus = parentBus
        
        # Identification 
        self.Area = int(newShunt.Area)
        self.Zone = int(newShunt.Zone)
        self.Id = str(newShunt.Id)
        
        # Properties
        #self.St = int(newShunt.St)
        self.B = ltd.data.single2float(newShunt.B) # PU Capacitance
        self.G = ltd.data.single2float(newShunt.G) # PU Inductance
        
        # From Bus information
        self.FBusnam = str(newShunt.GetBusName())
        self.FBusnum = int(newShunt.GetBusNumber())
        self.Fkv = ltd.data.single2float(newShunt.GetBusBasekv())

        # To Bus Information
        self.TBusnam = str(newShunt.GetToBusName())
        self.TBusnum = int(newShunt.GetToBusNumber())
        self.Tkv = ltd.data.single2float(newShunt.GetToBusBasekv())

        # Current Status
        self.cv={
            'St' : int(newShunt.St),
            }

    def __repr__(self):
        #Display more useful data for mirror
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s> " % (module,hex(id(self)))

        # additional outputs
        tag2 = "%s %s" %(str(self.FBusnum).zfill(3), self.FBusnam)
        # additional outputs
        tag3 = "%s %s" %(str(self.TBusnum).zfill(3), self.TBusnam)

        return(tag1+tag2+' to '+tag3)
