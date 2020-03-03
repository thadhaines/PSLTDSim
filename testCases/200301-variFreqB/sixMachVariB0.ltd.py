# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 2 2 : step St 2 0',
    ]

# Balancing Authorities
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B': "1.0 : permax", # MW/0.1 Hz
        'BVgain' : 0.0, # variable frequency bias gain
        'AGCActionTime': 30.00, # seconds 
        'ACEgain' : 2.0,
        'AGCType':'TLB : 2', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/10,
        'IACEdeadband' : 0, # System f Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : 0, # ACE MW
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 1 : 0.5 : rampA',
            'gen 2 1 : 0.5 : rampA',
                     ]
        },
    'BA2':{
        'Area':2,
        'B': "1.0 : permax", # MW/0.1 Hz
        'BVgain' : 0.0, # variable frequency bias gain
        'AGCActionTime': 30.00, # seconds 
        'ACEgain' : 2.0,
        'AGCType':'TLB : 2', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/10,
        'IACEdeadband' : 0, # System f Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : 0, # ACE MW
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': ['gen 3 : 1.0 : rampA',]
        },
    }