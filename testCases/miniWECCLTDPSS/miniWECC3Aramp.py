# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC Multi Area ramp of 1200 MW at t=2 to t=42 - PSS enabled in dyd
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 120,    
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
    'fileDirectory' : "\\delme\\miniWECC3ALTDPSS\\", # relative path from cwd
    'fileName' : 'miniWECCLTDPSSramp',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTDPSS.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTD_PSS.dyd"]
ltdPath = r".\testCases\miniWECCLTDPSS\miniWECCRamp.ltd.py"