# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

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
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': [
            'gen 1 : .20 ',
            'gen 9 : .20 ',
            'gen 17 : .20 ',
            'gen 23 : .20 ',
            'gen 118 : .20 ',
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
            'gen 68 : .50',
            'gen 71 : .50',
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
            'gen 41 : .20 ',
            'gen 48 : .20 ',
            'gen 59 : .20 ',
            'gen 60 : .20 ',
            'gen 65 : .20 ',
                    ]
        },
    }
