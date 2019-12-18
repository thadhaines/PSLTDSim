# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC trip of gen bus 27 at t=2, 
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
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
    'fileDirectory' : "\\delme\\thesisV\\", # relative path from cwd
    'fileName' : 'miniWECCgenTrip027PSS',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    'assumedV' : 'Vsched', # assummed voltage - either Vsched or Vinit
    'logBranch' : True,
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTD_PSS.dyd"]
ltdPath = r".\testCases\191217-thesisValidation\miniW\miniWECCgenTrip0.ltd.py"