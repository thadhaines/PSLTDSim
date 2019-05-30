# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Change the non-slack governed generator Pset point to -2 MW relative (48) at t=2
* Only goest to 49 -> governor action keeps gens on droop curve for both gens
* Ramp of other gen added to return f->1.

Adding a load ref might allow this to work the way you'd think...
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 60,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\ee554PsetStep\\", # relative path from cwd
    'fileName' : 'ee554PsetStep',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\eele554\tgov\ee554.sav"
dydPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.exc2Gov.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\eele554\tgov\ee554.PsetStep.ltd"]