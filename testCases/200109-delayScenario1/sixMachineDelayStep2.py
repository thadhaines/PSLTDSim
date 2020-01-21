# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
No AGC Response (no delay)
Delay over response test
Loss of generation in area 2 at t=2
Delayed action by area 1
AGC in both areas
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0, # seconds
    'endTime': 60.0*8, # seconds
    'slackTol': 1, # MW
    'PY3msgGroup' : 3, # number of Agent msgs per AMQP msg
    'IPYmsgGroup' : 60, # number of Agent msgs per AMQP msg
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Damping
    'fBase' : 60.0, # System F base in Hertz
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\200109-delayScenario1\\", # relative path from cwd
    'fileName' : 'SixMachineDelayStep2',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    'assumedV' : 'Vsched', # assummed voltage - either Vsched or Vinit
    'logBranch' : True,
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachineTrips.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachineDelay.dyd"]
ltdPath = r".\testCases\200109-delayScenario1\sixMachineDelayStep2.ltd.py"