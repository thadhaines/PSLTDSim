# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 5 : step Pm 2 -100 rel', # Step generator down
    ]

# Definite Time Controller Definitions
mirror.DTCdict = {
    'bpaTest' : {
        'RefAgents' : {
            'ra1' : 'mirror : f',
            'ra2' : 'gen 2 1 : R', 
            'ra3' : 'gen 2 1 : Pref0',
            'ra4' : 'gen 2 1 : Mbase',
            },# end Referenc Agents
        'TarAgents' : {
            'tar1' : 'gen 2 1 : Pref',
            }, # end Target Agents
        'Timers' : {
            'set' :{ # set Pref
                'logic' : "(ra1 > 0)", # should always eval as true
                'actTime' : 4, # seconds of true logic before act
                'act' : "tar1 = ra3 + (1-ra1)/ra2 * ra4 ", # step 
            },# end set
            'reset' :{ # not used
                'logic' : "0",
                'actTime' : 30, # seconds of true logic before act
                'act' : "0", # set any target On target = 0
            },# end reset
            'hold' : 0, # minimum time between actions
            }, # end timers
        },# end bpaTest
    }# end DTCdict
