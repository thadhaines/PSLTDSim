# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

ACEgain = 2.0

# Perturbances
mirror.sysPerturbances = [
    'load 43 : step P 2 200 rel',
    ]

mirror.govDelay ={
    'WA-GEN' : {
        'genBus' : 17,
        'genId' : None, # optional
        'wDelay' : (40,0),
        'PrefDelay' : (10, 0),
        },
    'ORE-G19' : {
        'genBus' : 19,
        'genId' : None, # optional
        'wDelay' : (40,0),
        'PrefDelay' : (10, 0),
        },
    'ORE-G23' : {
        'genBus' : 23,
        'genId' : None, # optional
        'wDelay' : (40,0),
        'PrefDelay' : (10, 0),
        },
    #end of defined governor delays
    }


mirror.sysBA = {
    'North':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 25.00, # seconds 
        'ACEgain' : ACEgain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/5,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 1 : .25 : rampA',
            'gen 17 : .25 : rampA',
            'gen 23 : .25 : rampA',
            'gen 118 : .25 : rampA',
            ]
        },
    'East':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 25.00, # seconds 
        'ACEgain' : ACEgain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/5,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 107 : .50 : rampA',
            'gen 71 : .50 : rampA',
            ]
        },
    'South':{
        'Area':3,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 25.00, # seconds 
        'ACEgain' : ACEgain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 15, # seconds - size of window - 0 for non window
        'IACEscale' : 1/5,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': [
            'gen 41 : .25 : rampA',
            'gen 48 : .25 : rampA',
            'gen 59 : .25 : rampA',
            'gen 65 : .25 : rampA',
            ]
        },
    }