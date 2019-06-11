# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Ramp load 30% from 2-87 seconds, open two lines from 7-8 (ck 1,2) at time 10.
Ramp removed from ltd -> branch tripping affects vars and f
Probably more interesting results in looking at current flow...
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 30,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\kundurRampBranch\\", # relative path from cwd
    'fileName' : 'kundurRampBranch0',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.sav"
dydPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur.rampBranch.ltd"]