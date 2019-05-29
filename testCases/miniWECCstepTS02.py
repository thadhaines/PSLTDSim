# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
MiniWECC step of +1200 MW at t=2. ts = 0.25
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.25,
    'endTime': 90,
    'slackTol': 1,
    'PY3msgGroup' : 5,
    'IPYmsgGroup' : 60,
    'Hsys' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\miniWECCstep\\", # relative path from cwd
    'fileName' : 'mwStepTS02',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
dydPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_loadStep.ltd"]