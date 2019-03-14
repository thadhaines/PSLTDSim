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

print('in IPY main')

### Start Simulation functions calls
ltd.init_PSLF(locations)

mir = ltd.mirror.Mirror(locations, simParams, 1)

mirLoc = ltd.data.saveMirror(mir, simParams)
print(mir)
## rando test
msg = {'msgType' : 'mirrorOk',
       'mirLoc' : mirLoc,
       'val': 'alls cool breh',}
IPY.send('toPY3', msg)

