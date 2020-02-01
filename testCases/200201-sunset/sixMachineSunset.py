# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
Sunset in the West
Loads increasing trend
Area 1 exporting 200 MW to Area 2 as IC0
Area 2 loses 27% of non-governed generation over 2 hours (sunset)
Shunts are configured to keep bus 8 and 9 Voltage betwee 0.95 and 1.05 PU
Governors on 4 Gens
AGC signals split to Area 1 gens, only act on 1 gen in Area 2
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 60.0*60*4,
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
    'fileDirectory' : "\\delme\\200201-sunset\\", # relative path from cwd
    'fileName' : 'sixMachineSunset',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    'assumedV' : 'Vsched', # assummed voltage - either Vsched or Vinit
    'logBranch' : True,
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachineLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachineLTD.dyd"]
ltdPath = r".\testCases\200201-sunset\sixMachineSunset.ltd.py"