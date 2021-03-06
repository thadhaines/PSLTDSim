# Format of required info for batch runs.
debug = 0
AMQPdebug = 0
debugTimer = 0

simNotes = """
MiniWECC Multi Area windramp
gen on bus 62 drops 1500 MW
3 BAs using standard ACE parameters for B 
'Bad Actor' Has a wind ramp - Using no deadband

AGC dispatched every 3 seconds
ACE gained by 3
IACE Included
no filter
*Ensure all controlled machines have governors!
"""

# Simulation Parameters Dictionary
simParams = {
    'timeStep': 1,
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
    'fileDirectory' : "\\delme\\IEEE\\", # relative path from cwd
    'fileName' : 'windrampNoDBFastGainIACENoFilter',
    'exportFinalMirror': 1, # Export mirror with all data
    'exportMat': 1, # if IPY: requies exportDict == 1 to work
    #'exportDict' : 0, # when using python 3 no need to export dicts.
    #'deleteInit' : 0, # Delete initialized mirror <- not implemented
    }

savPath = r"C:\LTD\pslf_systems\miniWECC\miniWECC3AreaLTD.sav"
dydPath = [r"C:\LTD\pslf_systems\miniWECC\miniWECC_LTDgov.dyd"]
ltdPath = r".\testCases\IEEEpaper\windrampNoDBFastGainIACENoFilter.ltd.py"