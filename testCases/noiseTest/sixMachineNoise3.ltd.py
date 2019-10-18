# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Uses Steps and no ACE filtering

# Perturbances
mirror.sysPerturbances = [
    #'load 9 : step P 5 75 rel',
    #'gen 5 : step Pm 5 -75 rel',
    #'gen 5 : step Pref 5 -75 rel',
    ]

# Power Plants
mirror.sysPowerPlants ={'pp1': ["gen 2 1: 0.75 : step", "gen 2 2 : 0.25: step"],
                        'pp2': ["gen 3 : 0.75: step", "gen 4 : 0.25: step"],
                        }

mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.3, True)

# Testing of Balancing Authority input
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B': "2.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds  
        'ACEgain' : 2.0,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window
        'IACEscale' : 1/15,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'nldroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': ['plant pp1 : .60 ',
                    'gen 1 : .40 : step']
        },
    'BA2':{
        'Area':2,
        'B': "2.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds  
        'ACEgain' : 2.0,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window
        'IACEscale' : 1/15,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'nldroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': ['plant pp2 : 1.0 ']
        },
    }
