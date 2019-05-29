# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Step load in mulit area GE 4 machine system. Tgov1 on all machines.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.25,
    'endTime': 45,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : -75, # PU; Experimental
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\ge4Step\\", # relative path from cwd
    'fileName' : 'ge4LoadStep',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"
dydPath = [r"C:\LTD\pslf_systems\GE_ex\g4_a.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\GE_ex\g4_loadStep.ltd"]