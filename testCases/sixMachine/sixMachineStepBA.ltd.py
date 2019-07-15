# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Uses Steps and no ACE filtering

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 5 75 rel',
    ]

# Power Plants
mirror.sysPowerPlants ={'pp1': ["gen 2 1: 0.75 : step", "gen 2 2 : 0.25: step"],
                        'pp2': ["gen 3 : 0.75: step", "gen 4 : 0.25: step"],
                        }

# Testing of Balancing Authority input
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 0', # Tie-Line Bias
        'Filtering': None,
        'DeadZone' : None,
        'CtrlGens': ['plant pp1 : .60 ',
                    'gen 1 : .40 : step']
        },
    'BA2':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 0', # Tie-Line Bias
        'Filtering': None,
        'DeadZone' : None,
        'CtrlGens': ['plant pp2 : 1.0 ']
        },
    }
