# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Step up in 3 bus 5 machine system.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 30,
    'slackTol': 1,
    'msgGroup' : 10, # not yet implemented
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\ee554Step\\", # relative path from cwd
    'fileName' : 'ee554noGovStepUp',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
dydPath = [r"C:\LTD\pslf_systems\eele554\ee554.excNoGov.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\eele554\ee554.BigUpStep.ltd"]