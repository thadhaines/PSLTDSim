# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
MiniWECC step of +1200 MW at t=2. ts = 0.5
Increasing both message sizes
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.5,
    'endTime': 90,
    'slackTol': 1,
    'PY3msgGroup' : 5,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # PU; 
    # Mathematical Options
    'freqEffects' : 1, # w in swing equation will not be assumed 1 if this is true
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\miniWECCstepMSG\\", # relative path from cwd
    'fileName' : 'mwStepMsgB',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTD.dyd"]
ltdPath = r".\testCases\miniWECC\miniWECCStep.ltd.py"