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
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 5.00, # seconds  
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : False,
        'IACEwindow' : 60, # seconds - size of window
        'IACEscale' : 1/45,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.036, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.025 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 17 : .5 : rampA',
            'gen 76 : .5 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 5.00, # seconds    # changed 10/6/19,
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : False,
        'IACEwindow' : 60, # seconds - size of window
        'IACEscale' : 1/45,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.036, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.025 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
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
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 5.00, # seconds    # changed 10/6/19
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : True,
        'AreaDroop' : .05, # this large R is meant to minimize gov action
        'IncludeIACE' : False,
        'IACEwindow' : 60, # seconds - size of window
        'IACEscale' : 1/45,
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.036, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.025 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
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