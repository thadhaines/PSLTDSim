# Format of required info for batch runs.
debug = 1
AMQPdebug = 0
debugTimer = 0

simNotes = """
Test system / scenario for testing generator Q limits in PSLF
Contrived example where Q limits are set very near initial values so that 
limits are hit relatively fast.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 0.5,
    'endTime': 60.0,
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
    'fileDirectory' : "\\delme\\200210-Qlim\\", # relative path from cwd
    'fileName' : 'sixMachineQlim',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    'assumedV' : 'Vsched', # assummed voltage - either Vsched or Vinit
    'logBranch' : True,
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachineLTDQlim.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachineLTD.dyd"]
ltdPath = r".\testCases\200210-QlimTest\sixMachineQlim.ltd.py"


"""
Results:
Slack bus Q cannot be limited.
Limiting of Q on other gens does in fact cause voltage to drop as Q remains at limit.
PF soln tends to hit iteration limit with multiple limited gens.
"""