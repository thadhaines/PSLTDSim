# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC Multi Area step of -1000 MW at t=2 on gen bus 62. ts = 1
Addition of 3 BAs
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 660,    
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
    'fileDirectory' : "\\delme\\miniWECC3A\\", # relative path from cwd
    'fileName' : 'miniWECC3A1',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC3Area.sav"
dydPath = [r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"]
ltdPath = r".\testCases\miniWECC3Area\miniWECC3A1.ltd.py"