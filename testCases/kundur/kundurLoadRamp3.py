# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Ramp of load down 30% over 40 seconds.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.25,
    'endTime': 80,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'ReffEnable' : False, # Account for Governor R being affected by non-gov %
    # Mathematical Options
    'freqEffects' : True, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\kundurRamp\\", # relative path from cwd
    'fileName' : 'kundurRamp3',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTD.sav"
dydPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur4LTDsameGens5.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\kundur4LTD\kundur.ramp0.ltd"]