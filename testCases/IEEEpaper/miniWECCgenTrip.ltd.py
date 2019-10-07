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
        'B':" 1.0 : p", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds    # changed 10/6/19
        'AGCType':'TLB : 2', # Tie-Line Bias # changed 10/6/19
        'IncludeIACE' : False,
        'IACEwidow' : 60, # seconds - size of window
        'IACEscale' : 1/60,
        'IACEdeadband' : 0.0015, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW?
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 17 : .5 : rampA',
            'gen 23 : .5 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds    # changed 10/6/19
        'AGCType':'TLB : 2', # Tie-Line Bias # changed 10/6/19
        'IncludeIACE' : False,
        'IACEwidow' : 60, # seconds - size of window
        'IACEscale' : 1/60,
        'IACEdeadband' : 0.0015, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW?
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 107 : .50 : rampA',
            'gen 71 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B':" 1.0 : p", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds    # changed 10/6/19
        'AGCType':'TLB : 2', # Tie-Line Bias # changed 10/6/19
        'IncludeIACE' : False,
        'IACEwidow' : 60, # seconds - size of window
        'IACEscale' : 1/60,
        'IACEdeadband' : 0.0015, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.04 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW?
        'GovDeadbandType' : 'NLDroop', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 48 : .5 : rampA',
            'gen 65 : .5 : rampA',
                    ]
        },
    }