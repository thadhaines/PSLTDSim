# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 25 : ramp Pm 2 1200 400 rel',
    ]

# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
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
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': [
            'gen 107 : .50 : rampA',
            'gen 71 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': [
            'gen 41 : .25 : rampA',
            'gen 48 : .25 : rampA',
            'gen 59 : .25 : rampA',
            'gen 65 : .25 : rampA',
                    ]
        },
    }
