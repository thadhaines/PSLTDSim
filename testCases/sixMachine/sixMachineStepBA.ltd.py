# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 5 10 per',
    #'load 9 : step P 70 -75 rel',
    ]

# Power Plants
#TODO: define ACE action of each plant in power plant, not in BA
mirror.sysPowerPlants ={'pp1': ["gen 2 1: 0.75", "gen 2 2 : 0.25"],
                        'pp2': ["gen 3 : 0.75", "gen 4 : 0.25"],
                        }

# Testing of Balancing Authority input
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 7.00,
        'Type':'TLB', # Tie-Line Bias
        'Filtering': None,
        'CtrlGens': ['plant pp1 : .60 : step',
                    'gen 1 : .40 : step']
        },
    'BA2':{
        'Area':2,
        'B':" 1.0 : p", # MW/0.1 Hz
        'ActionTime': 7.00,
        'Type':'TLB', # Tie-Line Bias
        'Filtering': None,
        'CtrlGens': ['plant pp2 : 1.0 : step']
        },
    }

# Testing of Timers
mirror.TimerInput = { 
        'busVCounter':"bus 8 : Vm : < 0.9501 : 30",
        'mirrorF': " mirror : f : < .998 : 3",
        }