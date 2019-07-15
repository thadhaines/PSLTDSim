# LTD simulation models / perturbances
# Perturbance Targets are case sensitive!
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
# Ramps
#ID stuff	Type 	Target 	Tstart 	Rtime 	RVal Rtype
# Steps
#ID stuff	Type 	Target 	Tstart 	Val 	Type


# Perturbances
mirror.sysPerturbances = [
    'load 16 : ramp P 2 10 4000',
    'load 21 : step P 2 400 rel',
    'load 26 : ramp P 2 40 4000',
    ]