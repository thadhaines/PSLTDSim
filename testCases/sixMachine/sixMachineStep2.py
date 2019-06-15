# Format of required info for batch runs.
debug = 0
AMQPdebug = 0

simNotes = """
Step of load down 5%.
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1.0,
    'endTime': 45.0,
    'slackTol': 1,
    'PY3msgGroup' : 3,
    'IPYmsgGroup' : 60,
    'Hinput' : 0.0, # MW*sec of entire system, if !> 0.0, will be calculated in code
    'Dsys' : 0.0, # Untested 
    'Reff' : False, # Account for Governor R being affected by non-gov %
    'freqEffects' : True, # w in swing equation will not be assumed 1 if true
    # Mathematical Options
    'integrationMethod' : 'rk45',
    # Data Export Parameters
    'fileDirectory' : "\\delme\\sixMachineStep\\", # relative path from cwd
    'fileName' : 'SixMachineStep2',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    'exportDict' : 0, # when using python 3 no need to export dicts.
    'deleteInit' : 0, # Delete initialized mirror
    }

savPath = r"C:\LTD\pslf_systems\sixMachine\sixMachine.sav"
dydPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachine2.dyd"]
ltdPath = [r"C:\LTD\pslf_systems\sixMachine\sixMachineStep.ltd"]