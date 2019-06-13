# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Ramp of load up 5% over 40 seconds.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 90,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.00, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\kundurRamp1\\", # relative path from cwd
    'fileName' : 'kundurRamp11',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.sav"
dydPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTDsameGens.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur.ramp1.ltd"]