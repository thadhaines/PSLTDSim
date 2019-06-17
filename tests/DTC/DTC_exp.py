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
mirLoc = os.path.abspath(os.path.join(dirname, '..','..','delme','sixMachineStep','SixMachineStep4F.mir'))
print(mirLoc)
mir = ltd.data.readMirror(mirLoc)

# system references (to be included in DTC class)
ts = mir.timeStep
f = mir.cv['f']

mir.debugTimer = True
"""
# Agent reference dictionary -> Input by User
aObj = { 'bus7Check':"bus 7 : Vm : > 0.95 : 30",
        'bus1Check':"bus 1 : Vm : < 0.95 : 30",
        'underdefined':"bus 1 : Vm : < 0.95 ",
        'nonExistantAgent':"bus 20 : Vm : < 0.95 : 30",
        'nonAttr':"bus 8 : V : < 0.95 : 30",
        'mirror': " mirror : t : > 0 : 0",
        #'cap1': "shunt 8 1 : St ",
        }

# empty dictionary for mirror references
mObj = {}
for ref in aObj:
    """
    idStr = aObj[ref].split(":")[0].split() # split at spaces
    attr = aObj[ref].split(":")[1].strip() # remove extra whitespace
    condition = aObj[ref].split(":")[2].strip()
    actTime = aObj[ref].split(":")[3].strip()
    # debug
    #print("Id String: %s" % idStr)
    #print("Attribute: %s" % attr)
    #print("condition: %s" % condition)
    #print("actTime: %s" % actTime)
    
    foundAgent = ltd.find.findAgent(mir,idStr[0], idStr[1:] )
    if foundAgent:
        print('Found', foundAgent)
        mObj[ref] = foundAgent
        #print('Current %s value: %f' % (attr, foundAgent.cv[attr]))
        # Logic check
        print('Testing '+ref)
        if eval(str(foundAgent.cv[attr])+condition):
            print(str(foundAgent.cv[attr])+condition,' is true')
        else:
            print(str(foundAgent.cv[attr])+condition,' is False')
    """

    ### Testing of Timer Agent Init
    a = ltd.systemAgents.TimerAgent(mir,ref, aObj[ref]) 
    print(a)
    a.step()

# todo: Handle parsing logic to control 