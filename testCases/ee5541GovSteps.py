# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Step up and down in 3 bus 5 machine system with one gov on slack.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 60,
    'slackTol': 1,
    'msgGroup' : 10, # not yet implemented
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\ee554Steps\\", # relative path from cwd
    'fileName' : 'ee5541GovSteps',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.exc1Gov.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.steps.ltd"]