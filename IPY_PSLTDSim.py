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
# NOTE: host not sent over command as a simplification
host = '127.0.0.1'
IPY = ltd.amqp.AMQPAgent('IPY', host)

# receive init message
IPY.receive('toIPY',IPY.redirect)

print('in IPY main') # DEBUG

# Initialize PSLF and mirror
ltd.init_PSLF(locations)

mir = ltd.mirror.Mirror(locations, simParams, simNotes, debug, AMQPdebug)
IPY.mirror = mir

mirLoc = ltd.data.saveMirror(mir, simParams)

# Send mirror location to PY3
msg = {'msgType' : 'mirrorOk',
       'mirLoc' : mirLoc,
       }
IPY.send('toPY3', msg)

# begin IPY simulation loop
ltd.runSim_IPY(mir, IPY)