# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
Trip 2 Lines at t=2
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.5,
    'endTime': 90.0,
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
    'fileDirectory' : "\\delme\\sixMachineTrip\\", # relative path from cwd
    'fileName' : 'SixMachineBTrip0',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachineTrips.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachine2.dyd"]
ltdPath = r".\testCases\sixMachine\sixMachineBTrip0.ltd.py"