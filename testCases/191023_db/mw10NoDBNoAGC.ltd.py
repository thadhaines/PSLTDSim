# mw ACE base case
deadBandType = 'none'
aceGain = 0.0

# Perturbances
mirror.sysPerturbances = [
    # 1% of load = 1510.275 MW
    #'gen 62 : step Pm 2 -1510 rel',
    #'gen 62 : step Pref 2 -1510 rel',
    ]

mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True)

# Balancing Authority Input
mirror.sysBA = {
    'North':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 15.00, # seconds 
        'ACEgain' : aceGain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEdeadband' : 0.0, # Hz 
        'ACEFiltering': 'PI : 0.025 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : deadBandType, # step, none, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 17 : .25 : rampA',
            'gen 23 : .75 : rampA',
                    ]
        },
    'East':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 15.00, # seconds 
        'ACEgain' : aceGain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEdeadband' : 0.0, # Hz 
        'ACEFiltering': 'PI : 0.025 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : deadBandType, # step, none, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 30 : .50 : rampA',
            'gen 32 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 15.00, # seconds 
        'ACEgain' : aceGain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEdeadband' : 0.0, # Hz 
        'ACEFiltering': 'PI : 0.025 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : deadBandType, # step, none, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 45 : .33333 : rampA',
            'gen 53 : .33333 : rampA',
            'gen 59 : .33333 : rampA',
                    ]
        },
    }