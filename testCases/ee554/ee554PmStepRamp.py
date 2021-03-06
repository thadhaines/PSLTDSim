# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Change the non-governed generator Pm by -5% at t=2 
then ramp back to 50 mw  over 20 seconds starting at t=20
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 60,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\ee554PmStepRamp\\", # relative path from cwd
    'fileName' : 'ee554PmStepRamp',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\eele554\tgov\ee554.sav"
dydPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.exc1Gov.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.PmStepRamp.ltd"]