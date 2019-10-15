#Ramping wind in area 2
# Perturbances
mirror.sysPerturbances = [
    'gen 74 : ramp Pm 2 1200 400 rel',
    ]


# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 3.00, # seconds  
        'ACEgain' : 1.0,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 30, # seconds - size of window
        'IACEscale' : 1/60,
        'IACEuseWeight' : False, 
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.03 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 17 : .5 : rampA',
            'gen 76 : .5 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 3.00, # seconds    # changed 10/6/19,
        'ACEgain' : 1.0,
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : True,
        'AreaDroop' : 0.2,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/60,
        'IACEuseWeight' : False, 
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.03 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 30 : .50 : rampA',
            'gen 32 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B': "1.0 : permax", # MW/0.1 Hz
        'AGCActionTime': 3.00, # seconds    # changed 10/6/19
        'ACEgain' : 1.0,
        'AGCType':'TLB : 0', # Tie-Line Bias # changed 10/6/19
        'UseAreaDroop' : False,
        'AreaDroop' : .2, # this large R is meant to minimize gov action
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 30, # seconds - size of window
        'IACEscale' : 1/60,
        'IACEuseWeight' : False, 
        'IACEweight' : .3, # out of one - percent to mix with calculated ace
        'IACEdeadband' : 0.0, # Hz # changed 10/6/19
        'ACEFiltering': 'PI : 0.03 0.0001', # changed 10/6/19
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # changed 10/6/19
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # changed 10/6/19
        'GovBeta' : 0.036, # changed 10/6/19
        'CtrlGens': [
            'gen 45 : .333 : rampA',
            'gen 53 : .333 : rampA',
            'gen 59 : .333 : rampA',
                    ]
        },
    }