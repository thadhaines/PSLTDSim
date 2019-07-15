# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC Multi Area ramp of pm on gen 25 (+400 MW over 1200 seconds)
3 BAs using type 0 TLB 
(both tie line and freq ACE distributed according to w deviation)
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 2520,    
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
    'fileDirectory' : "\\delme\\BA\\", # relative path from cwd
    'fileName' : 'miniWECC3A4',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTD.dyd"]
ltdPath = r".\testCases\BA_tests\miniWECC3A4.ltd.py"