# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 2 10 per',
    ]

# Power Plants
mirror.sysPowerPlants ={'pp1': ["gen 2 1: 0.25", "gen 2 2 : 0.75"],
                        'pp2': ["gen 3 : 0.5", "gen 4 : 0.5"],
                        }

# Testing of Timers
mirror.TimerInput = { 
        'busVCounter':"bus 8 : Vm : < 0.9501 : 30",
        'mirrorF': " mirror : f : < .998 : 3",
        }

# Testing of Balancing Authority input
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 5.00,
        'Type':'TLB', # Tie-Line Bias
        'Filtering': None,
        'CtrlGens': ['plant pp1 : .65 : step',
                    'gen 1 : .35 : step']
        },
    'BA2':{
        'Area':2,
        'B':" 1 : p", # MW/0.1 Hz
        'ActionTime': 8.00,
        'Type':'TLB', # Tie-Line Bias
        'Filtering': None,
        'CtrlGens': ['gen 4: .5 : step',
                     'gen 5: .5 : step']
        },
    }