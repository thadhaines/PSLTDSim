class WindowIntegratorAgent(object):
    """A window integrator that initializes a history of window
    values, then updates the total window area each step."""

    def __init__(self, mirror, length):
        # Retain Inputs / mirror reference
        self.mirror = mirror
        self.length = length # length of window in seconds

        self.windowSize = int(self.length / self.mirror.timeStep)

        self.window = [0.0]*self.windowSize

        self.cv = {
            'windowInt' : 0.0,
            'totalInt' : 0.0,
            }

    def step(self, curVal, preVal):
        # calculate current window Area, return value
        t = self.mirror.cv['dp'] # current data point

        windowNDX = t % self.length

        oldVal = self.window[windowNDX]
        newVal = (curVal + preVal)/ 2.0 * self.mirror.timeStep

        self.window[windowNDX] = newVal
        self.cv['windowInt'] += newVal - oldVal
        self.cv['totalInt'] += newVal

        return self.cv['windowInt']


