# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 62 : step Pm 2 -1000 rel',
    'gen 62 : step Pref 2 -1000 rel',
    ]
"""
# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': ['plant pp1 : .60 ',
                    'gen 1 : .40 : rampA']
        },
    'East':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': ['plant pp2 : 1.0 ']
        },
    'South':{
        'Area':3,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.04 0.0001',
        'Deadband' : None,
        'CtrlGens': ['plant pp2 : 1.0 ']
        },
    }
"""