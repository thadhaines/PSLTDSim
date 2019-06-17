# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPert = [
    'load 9 : step P 2 10 per',
    ]

# Testing of Timers
mirror.TimerInput = { 
        'busVCounter':"bus 8 : Vm : < 0.9501 : 30",
        'mirrorF': " mirror : f : < .998 : 3",
        }