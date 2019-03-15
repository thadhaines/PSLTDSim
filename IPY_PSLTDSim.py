"""Ironpython main File"""
import os
import subprocess
import signal
import time
import __builtin__

# import custom package and make truly global
import psltdsim as ltd
__builtin__.ltd = ltd

# init IPY AMQP
# NOTE: host not sent over command to simplify future coding
host = '127.0.0.1'
IPY = ltd.amqp.AMQPAgent('IPY', host)

# receive init message
IPY.receive('toIPY',IPY.redirect)

print('in IPY main') # DEBUG

### Start Simulation functions calls
ltd.init_PSLF(locations)

mir = ltd.mirror.Mirror(locations, simParams, simNotes, debug)

mirLoc = ltd.data.saveMirror(mir, simParams)
time.sleep(0.1) # to ensure mirror closed.

# Send mirror location to PY3
msg = {'msgType' : 'mirrorOk',
       'mirLoc' : mirLoc,
       }
IPY.send('toPY3', msg)

## begin IPY simulation loop (probably part of mirror funciton)

# Hand off control to PY3 - consume LTD messages

# test refactored runSim_OG -> works!
#ltd.mirror.runSim_OG(mir)
#ltd.terminal.dispSimResults(mir)
