# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 5 : step Pm 20 -100 rel', # Step generator down
    ]

mirror.govDelay ={
    'delaygen1' : {
        'genBus' : 2,
        'genId' : '1', # optional
        'wDelay' : (0, 0, 1.0),
        'PrefDelay' : (0, 0)
        },
    #end of defined governor delays
    }