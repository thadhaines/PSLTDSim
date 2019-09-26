# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored
# IACE included

# Perturbances
mirror.sysPerturbances = [
    'gen 62 : step Pm 2 -1000 rel',
    'gen 62 : step Pref 2 -1000 rel',
    ]

# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 120, # seconds
        'Type':'TLB : 2', # Tie-Line Bias
        'IncludeIACE' : True,
        'IACEwidow' : 120, # seconds - size of window
        'IACEscale' : 1/500,
        'IACEdeadband' : 30E-6, # Pu Hz
        'Filtering': 'PI : 0.04 0.0001',
        'AGCDeadband' : None, # MW?
        'GovDeadband' : .036, # Hz
        'CtrlGens': [
            'gen 1 : .25 : rampA',
            'gen 17 : .25 : rampA',
            'gen 23 : .25 : rampA',
            'gen 118 : .25 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 120, # Seconds
        'Type':'TLB : 2', # Tie-Line Bias
        'IncludeIACE' : True,
        'IACEwidow' : 120, # seconds - size of window
        'IACEscale' : 1/500,
        'IACEdeadband' : 30E-6, # Pu Hz
        'Filtering': 'PI : 0.04 0.0001',
        'AGCDeadband' : None, # MW?
        'GovDeadband' : .036, # Hz
        'CtrlGens': [
            'gen 107 : .50 : rampA',
            'gen 71 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 120, # seconds
        'Type':'TLB : 2', # Tie-Line Bias
        'IncludeIACE' : True,
        'IACEwidow' : 120, # seconds - size of window
        'IACEscale' : 1/500,
        'IACEdeadband' : 30E-6, # Pu Hz
        'Filtering': 'PI : 0.04 0.0001',
        'AGCDeadband' : None, # MW?
        'GovDeadband' : .036, # Hz
        'CtrlGens': [
            'gen 41 : .25 : rampA',
            'gen 48 : .25 : rampA',
            'gen 59 : .25 : rampA',
            'gen 65 : .25 : rampA',
                    ]
        },
    }