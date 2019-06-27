# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Uses PI control and Distribution Ramps, TLB 2

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 5 75 rel',
    ]

# Power Plants
mirror.sysPowerPlants ={'pp1': ["gen 2 1: 0.75 : rampA", "gen 2 2 : 0.25: rampA"],
                        'pp2': ["gen 3 : 0.75: rampA", "gen 4 : 0.25: rampA"],
                        }

# Testing of Balancing Authority input
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.1 0.0001',
        'Deadband' : None,
        'CtrlGens': ['plant pp1 : .60 ',
                    'gen 1 : .40 : rampA']
        },
    'BA2':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB : 2', # Tie-Line Bias
        'Filtering': 'PI : 0.1 0.0001',
        'Deadband' : None,
        'CtrlGens': ['plant pp2 : 1.0 ']
        },
    }