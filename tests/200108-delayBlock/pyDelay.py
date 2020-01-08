# python delay block using numpy....


import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import psltdsim as ltd

# delay agent..
class DelayAgent(object):
    """
    An agent that delays input by x samples
    also applies additional filtering if specified

    of the form exp(-$d1)/(1+$T1)
    """

    def __init__(self, timestep, initVal, d1,t1):

        self.d1 = d1
        self.t1 = t1
        
        self.bufferSize = int(self.d1/timestep)

        self.buffer = [initVal]*self.bufferSize
        self.ndx = 0

        if t1 != 0.0:
            self.filter = None # use lowPassAgent
        else:
            self.filter = None
            
    def step(self, t, inputVal):
        """
        Handle putting input into buffer,
        reuturning correct value
        filtering if required
        """
        buffNDX = t % self.bufferSize
        outVal = self.buffer[buffNDX]

        self.buffer[buffNDX] = inputVal

        if self.filter != None:
            outVal = self.filter.stepFilter(outVal)

        return outVal

testDelay = DelayAgent(1,-1,4,0)

t = range(0,20,1)

print("T V")
for val in t:
    out = testDelay.step( val, val)
    print(val, out)

""" Result
Delay seems to work
Have to integrate into psltdsim and test
"""
