# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

CTRLtimeScale = 60*60 # ninutes

# Perturbances
mirror.sysPerturbances = [
    #'load 8 : step P 2 12 per',
    #'load 9 : step P 2 18 per',
    'gen 5 : ramp Pm 3600 10800 -20 rel' # 2 hour ramp starting at 1 hour
    ]
mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True)

# Controlled Shunt Definitions
mirror.ShuntControl = {
    'bus8Caps' : {
        # Fast Caps in Area 1
        'RefAgentType' : 'bus',
        'RefAgentID' : '8',
        'SetLogic' : 'Vm : <0.95',
        'SetTime' : 10, # seconds
        'SetCountType' : 'abs', # Type of counter to trigger
        'ResetLogic' : 'Vm : >1.05',
        'ResetTime' : 5, # seconds
        'ResetCountType' : 'abs',
        'HoldTime' : 20, # seconds, minimum time between actions
        'CtrlShunts' : [
            "shunt 8 2",
            "shunt 8 3",
            "shunt 8 4",
            "shunt 8 5",
            "shunt 8 6",
            ],
        },# end agend def
    'bus9Caps' : {
        # slow caps in area 2
        'RefAgentType' : 'bus',
        'RefAgentID' : '9',
        'SetLogic' : 'Vm : <0.95',
        'SetTime' : 25, # seconds
        'SetCountType' : 'abs', # Type of counter to trigger
        'ResetLogic' : 'Vm : >1.05',
        'ResetTime' : 10, # seconds
        'ResetCountType' : 'abs',
        'HoldTime' : 60, # seconds, minimum time between actions
        'CtrlShunts' : [
            "shunt 9 2",
            "shunt 9 3",
            "shunt 9 4",
            "shunt 9 5",
            "shunt 9 6",
            ],
        }, # end agent def
    }# end agents def

# Balancing Authorities
mirror.sysBA = {
    'BA1-BPAT':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 20.00, # seconds 
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
        'CtrlGens': ['gen 1 : 0.75 : rampA',
                     'gen 2 1 : 0.25 : rampA',
                     ]
        },
    'BA2-CAISO':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 10.00, # seconds 
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
        'CtrlGens': ['gen 3 : 1.0 : rampA',]
        },
    }
# Load and Generation Cycle Agents



mirror.sysGenerationControl = {
    'BPATDispatch' : {
        'Area': 1,
        'startTime' : 2,
        'timeScale' : CTRLtimeScale,
        'rampType' : 'per', # relative percent change
        'CtrlGens': [
            "gen 1 : 0.5",
            "gen 2 1 : 0.5", 
            ],
        # Data from: 12/11/2019 PACE
        'forcast' : [ 
            #(time , Precent change from previous value)
            (0, 0.0),
            (1, 5.8),
            (2, 8.8),
            (3, 9.9),
            (4, 4.0),
            ],
        }, #end of generation controller def
    'CAISODispatch' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : CTRLtimeScale,
        'rampType' : 'per', # relative percent change
        'CtrlGens': [
            "gen 3 : 0.5",
            "gen 4 : 0.5", 
            ],
        # Data from: 12/11/2019 PACE
        'forcast' : [ 
            #(time , Precent change from previous value)
            (0, 0.0),
            (1, 0.7),
            (2, 7.5),
            (3, 11.2),
            (4, 4.4),
            ],
        }, #end of generation controller def
    }


mirror.sysLoadControl = {
    'BPATDemand' : {
        'Area': 1,
        'startTime' : 2,
        'timeScale' : CTRLtimeScale,
        'rampType' : 'per', # relative percent change
        # Data from: 12/11/2019 BPAT
        'demand' : [ 
            #(time , Precent change from previous value)
            (0, 0.000),
            (1, 3.2),
            (2, 8.2),
            (3, 9.3),
            (4, 3.8),
        ] ,
    }, # end of demand agent def
    'CAISODemand' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : CTRLtimeScale,
        'rampType' : 'per', # relative percent change
        # Data from: 12/11/2019 CAISO
        'demand' : [ 
            #(time , Precent change from previous value)
            (0, 0.000),
            (1, 3.0),
            (2, 7.0),
            (3, 10.5),
            (4, 4.4),
        ] ,
    },# end of demand load control definition
}# end of loac control definitions

