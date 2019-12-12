# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
Full wecc, step load on bus 24902 up 10% at t=2 (~60 MW increase)
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
    'endTime': 30,    
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'fBase' : 60.0, # System F base in Hertz
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    'mainIsland' : 1, # if >0, ignore all objects not in main island
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\fullWECC\\", # relative path from cwd
    'fileName' : 'fWECCstep',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 0, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

#savPath = r"C:\LTD\pslf_systems\fullWecc\mysteryWECC\fullWecc.sav"
#dydPath = [r"C:\LTD\pslf_systems\fullWecc\mysteryWECC\fullWeccFixed.dyd"]
savPath = r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a.sav"
dydPath = [r"C:\LTD\pslf_systems\fullWecc\18HSP\18HSP2a1Fixed.dyd"]
ltdPath = r".\testCases\191122-fullWECC\fWECCStep.ltd.py"