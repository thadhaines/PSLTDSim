# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored
# IACE included

# Perturbances
mirror.sysPerturbances = [
    'gen 62 : step Pm 2 -1500 rel',
    'gen 62 : step Pref 2 -1500 rel',
    ]

# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 20.00, # seconds  
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
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 17 : .25 : rampA',
            'gen 23 : .75 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 20.00, # seconds    # changed 10/6/19,
        'ACEgain' : 2.0,
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 30 : .50 : rampA',
            'gen 32 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 20.00, # seconds    # changed 10/6/19
        'ACEgain' : 2.0,
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : False,
        'AreaDroop' : .2, # this large R is meant to minimize gov action
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window
        'IACEscale' : 1/15,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 45 : .333 : rampA',
            'gen 53 : .333 : rampA',
            'gen 59 : .333 : rampA',
                    ]
        },
    }