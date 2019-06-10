""" Experimenting with possible forms of a definite time controller that
uses arbitrary sting inputs to execute logic that then alters agent values
inside the system mirror """
import os
import time # for poorly nested timings...

import psltdsim as ltd
# for global library
import builtins
builtins.ltd = ltd
builtins.time = time

# read some mirror
dirname = os.path.dirname(__file__)
print(dirname)
os.chdir(dirname)
# abspath required to process the '..' used in the relative path
mirLoc = os.path.abspath(os.path.join(dirname, '..','..','delme','kundurRamp','kundurRamp2F.mir'))
print(mirLoc)
mir = ltd.data.readMirror(mirLoc)

# system references (to be included in DTC class)
ts = mir.timeStep
f = mir.cv['f']

# Agent reference dictionary -> Input by User
aObj = { 'bus1':"bus 7 : Vm ",
        'cap1': "shunt 7 1 : St "}

logic = [
    "'set' += ts if 'bus1' < 0.95 else 'set' = 0",
    "'cap1' = 1 if set > 30"
    ]
timers = {
    'set':0, 'reset': 0, 'delay':0
    }
# empty dictionary for mirror references
mObj = {}
for ref in aObj:
    idStr = aObj[ref].split(":")[0].split() # split at spaces
    attr = aObj[ref].split(":")[1].strip() # remove extra whitespace
    #print("Id String: %s" % idStr)
    #print("Attribute: %s" % attr)
    foundAgent = ltd.find.findAgent(mir,idStr[0], idStr[1:] )
    if foundAgent:
        print('Found', foundAgent)
        mObj[ref] = foundAgent
        print('Current %s value: %f' % (attr, foundAgent.cv[attr]))

# todo: Handle parsing logic to control 