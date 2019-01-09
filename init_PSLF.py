def init_PSLF(self):
        """Initialize instance of PSLF with given paths. 
        Returns pslf object, prints error code, or crashes.
        """
        # create pslf instance / object
        pslf = mid.Pslf(self.locations[1])   
        # load .sav file
        load_test = pslf.LoadCase(self.locations[2])     

        if load_test == 0:
            print(self.locations[2] + " Successfully loaded.")
            return pslf
        else:
            print("Failure to load .sav")
            print("Error code: %d" % test)
            return None