# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored
# Double quoted variable names in sysPert parameters ignored

# Perturbances
mirror.sysPerturbances = [
    'gen 2 2 : step Pm 2 -20 per',
    ]

mirror.govDelay ={
    'delaygen3' : {
        'genBus' : 3,
        'genId' : None, # optional
        # (delay param, filter param, gain)
        'wDelay' : (0,10),
        'PrefDelay' : (0, 10),
        },
    #end of defined governor delays
    }

# untested deadband options....
mirror.govDeadBand ={
    'gen3DB' : {
        'genBus' : 3,
        'genId' : None, # optional
        'GovDeadbandType' : 'ramp', # step, ramp, nldroop
        'GovDeadband' : 0.036, # Hz
        'GovAlpha' : 0.016, # Hz, used for nldroop
        'GovBeta' : 0.036, # Hz, used for nldroop
        },
    'gen1DB' : {
        'genBus' : 1,
        'genId' : None, # optional
        'GovDeadbandType' : 'nldroop', # step, ramp, nldroop
        'GovDeadband' : 0.036, # Hz
        'GovAlpha' : 0.016, # Hz, used for nldroop
        'GovBeta' : 0.036, # Hz, used for nldroop
        },
    'gen4DB' : {
        'genBus' : 4,
        'genId' : None, # optional
        'GovDeadbandType' : 'step', # step, ramp, nldroop
        'GovDeadband' : 0.036, # Hz
        'GovAlpha' : 0.016, # Hz, used for nldroop
        'GovBeta' : 0.036, # Hz, used for nldroop
        },
    #end of defined governor deadbands
    }

mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 5.00, # seconds 
        'ACEgain' : 2.0,
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
        'CtrlGens': ['gen 1 : 1 : rampA']
        },
    'BA2':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 5.00, # seconds 
        'ACEgain' : 2.0,
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
        'CtrlGens': ['gen 3 : 1.0 : rampA']
        },
    }
