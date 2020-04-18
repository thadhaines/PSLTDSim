# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
2018 Heavy Spring WECC, 100 MW load ramp on buses 24160, 24133, 24135 when t=2-42 
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 90, 
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'fBase' : 60.0, # System F base in Hertz
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    'mainIsland' : 1, # if >0, ignore all objects not in main island
    'assumedV' : 'V0', # work around for WECC
    'logBranch' : False,
    'makeXFMRs' : False, # work around for islanded WECC xfmrs
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\thesisV\\", # relative path from cwd
    'fileName' : 'wecc18HSPRamp',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2aEDIT.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1Fixed.dyd"]
ltdPath = r".\testCases\191217-thesisValidation\wecc\18HSPweccRamp.ltd.py"