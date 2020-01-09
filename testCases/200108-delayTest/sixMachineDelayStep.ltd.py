# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 3 : step Pref 2 10 per',
    'gen 3 : step Pref 10 -10 per',
    ]

mirror.govDelay ={
    'delaygen3' : {
        'genBus' : 3,
        'genId' : None, # optional
        'wDelay' : (0,0),
        'PrefDelay' : (2, 0),
        },
    #end of defined governor delays
    }
