# python delay block using numpy....

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import psltdsim as ltd

# delay agent...
class DelayAgent(object):
    """
    An agent that delays input by x samples
    and applies additional filtering if specified
    of the form: outVal = inVal * exp(-$d1)/(1+$t1)
    where d1 is a time delay that is divisible by the timestep 
    (Note: d1 can not be less than the timestep)
    and t1 is the time constant for the lowpass filter
    """

    def __init__(self, timestep, initVal, d1,t1):

        #TODO: get mirror and agent references, use gen values for init
        self.ts = timestep
        self.d1 = d1 # delay time constant
        self.t1 = t1 # filter time constant
        
        self.bufferSize = int(self.d1/timestep)

        self.buffer = [initVal]*self.bufferSize

        if self.bufferSize == 0:
            print("*** Delay Error. bufferSize == 0...")

        if t1 != 0.0:
            self.filter = None # use lowPassAgent
        else:
            self.filter = None
            
    def step(self, t, inputVal):
        """
        Handle buffer output/input, 
        filtering if required
        """
        buffNDX = int(t/self.ts % self.bufferSize)
        outVal = self.buffer[buffNDX-1]

        self.buffer[buffNDX] = inputVal

        if self.filter != None:
            outVal = self.filter.stepFilter(outVal)

        return outVal

ts = 1
initVal = -1
d1 = 2
t1 = 0
tEnd = 6
testDelay = DelayAgent(ts,initVal,d1,t1)

t = np.arange(0,tEnd,ts)

print("T V")
for val in t:
    out = testDelay.step( val, val)
    print(val, out)

""" Result
Delay seems to work well
Have to integrate into psltdsim and test
"""
