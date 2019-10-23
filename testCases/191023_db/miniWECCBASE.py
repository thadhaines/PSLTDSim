# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC base case for noise testing
"""
timeStep = 1.0
fileName = 'mw10Base'
ltdPath = r".\testCases\191023_db\miniWECCBASE.ltd.py"

# Simulation Parameters Dictionary
simParams = {
    'timeStep': timeStep,
    'endTime': 1800,    
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'fBase' : 60.0, # System F base in Hertz
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\191023-db\\", # relative path from cwd
    'fileName' : fileName,
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1,
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTDgov.dyd"]