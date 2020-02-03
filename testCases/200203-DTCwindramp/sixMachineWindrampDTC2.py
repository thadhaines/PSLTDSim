# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
Multi hour windramp to show shunt control
Loads manipulated to follow windramp
Area 1 exporting 200 MW to Area 2 as IC0
Normal dispatch for 10 min, 45 min ramp up, 10 min hold, 45 min ramp down, 10 resolution = 2 hour sim
Shunts are configured to keep bus 8 and 9 Voltage between 1 and 1.04 PU
Additionally, line flow is motitored to switch bus 9 shunts if Mvar > 13, and off if Mvar < 13 (per line)
Governors on 4 Gens (non ramping gens)
AGC signals split to Area 1 gens, only act on gen 3 in Area 2
Area 2 shunts and AGC slightly slower than area 1
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 60.0*60*2,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'fBase' : 60.0, # System F base in Hertz
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\200203-DTCwindramp\\", # relative path from cwd
    'fileName' : 'sixMachineWindramp2',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    'assumedV' : 'Vsched', # assummed voltage - either Vsched or Vinit
    'logBranch' : True,
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachineLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachineLTD.dyd"]
ltdPath = r".\testCases\200203-DTCwindramp\sixMachineWindrampDTC2.ltd.py"