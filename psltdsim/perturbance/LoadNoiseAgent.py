class LoadNoiseAgent(object):
    """
    Add random noise to real power of loads...
    Should Q also move?
    """

    def __init__(self, mirror, percNoise, walk=False, damping=0, seed=42):
        # Save init values to object
        self.mirror = mirror
        self.percNoise = percNoise/100.00 # percent of noise
        self.walk = walk
        self.damping = damping
        self.seed = seed

        # Seed random number generator
        np.random.seed(seed)

    def __repr__(self):
        """Display more useful data for mirror"""
        # mimic default __repr__
        T = type(self)
        module = T.__name__
        tag1 =  "<%s object at %s>\n" % (module,hex(id(self)))

        # additional outputs
        tag2 = "Adding %s%% noise to loads. Seed = %.2f" %(
            self.self.percNoise,
            self.seed,
            )

        return(tag1+tag2)

    def step(self):
        """Function called every timestep"""
        for load in self.mirror.Load:

            # Skip loads that are off
            if load.cv['St'] == 0:
                continue

            oldVal = load.cv['P']

            # Get Starting Value
            if self.walk:
                seedVal = load.cv['P']
            else:
                seedVal = load.cv['Psched']

            #Choose if adding or subtracting noise
            if np.random.randint(2): # returns a 1 or 0
                #subtract
                noise = -self.percNoise*np.random.ranf()
            else:
                #add
                noise = self.percNoise*np.random.ranf()

            # Calculate damping
            freqDamping = self.damping*self.mirror.cv['deltaF']
            # Calculate new value
            newVal = round(seedVal*(1.0 + noise + freqDamping),4)
            # Calculate deltaP
            deltaP = newVal-oldVal
            # Set Load to new random value
            load.cv['P'] = newVal
            # Account for delta in mirror
            self.mirror.ss_Pert_Pdelta += deltaP

            # Send AMQP message about change to IPY
            send_start = time.time()
            self.mirror.PY3.send('toIPY', load.makeAMQPmsg())
            self.mirror.PY3SendTime += time.time() -send_start
            self.mirror.PY3msgs+=1
