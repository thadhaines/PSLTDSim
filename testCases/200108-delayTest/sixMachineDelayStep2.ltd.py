# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 2 10 per',
    ]

mirror.govDelay ={
    'delaygen3' : {
        'genBus' : 3,
        'genId' : None, # optional
        'wDelay' : (2,0),
        'PrefDelay' : (0, 0),
        },
    #end of defined governor delays
    }
