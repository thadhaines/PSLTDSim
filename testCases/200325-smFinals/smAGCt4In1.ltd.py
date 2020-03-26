# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

CTRLtimeScale = 60*60 # ninutes

# Perturbances
mirror.sysPerturbances = [
    # AGC steps
    'gen 2 2 : step Pm 2 -150 rel',
    #'gen 5 : step Pm 2 -150 rel',
    # ramp non-gov gens
    #'gen 2 2 : ramp Pm 600 2700 150 rel', # 45 min ramp up
    #'gen 2 2 : ramp Pm 3900 2700 -150 rel', # 45 min ramp down
    #'gen 5 : ramp Pm 600 2700 300 rel', # 45 min ramp up
    #'gen 5 : ramp Pm 3900 2700 -300 rel', # 45 min ramp down
    ]

mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.05, walk=True, delay=0, damping=0, seed=11)

# Balancing Authorities
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B': "0.9 : permax", # MW/0.1 Hz
        'AGCActionTime': 30.00, # seconds 
        'ACEgain' : 1.0,
        'AGCType':'TLB : 4', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': True,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/5,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'none', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': ['gen 1 : 0.5 : rampA',
                     'gen 2 1 : 0.5 : rampA',
                     ]
        },
    'BA2':{
        'Area':2,
        'B': "0.9 : permax", # MW/0.1 Hz
        'AGCActionTime': 45.00, # seconds 
        'ACEgain' : 1.0,
        'AGCType':'TLB : 4', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': True,
        'IACEwindow' : 45, # seconds - size of window - 0 for non window
        'IACEscale' : 1/3,
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


"""
# Definite Time Controller Definitions
mirror.DTCdict = {
    'bus8caps' : {
        'RefAgents' : {
            'ra1' : 'bus 8 : Vm',
            'ra2' : 'branch 8 9 1 : Qbr', # branches defined from, to, ckID
            },# end Referenc Agents
        'TarAgents' : {
            'tar1' : 'shunt 8 2 : St',
            'tar2' : 'shunt 8 3 : St',
            'tar3' : 'shunt 8 4 : St',
            'tar4' : 'shunt 8 5 : St',
            'tar5' : 'shunt 8 6 : St',
            }, # end Target Agents
        'Timers' : {
            'set' :{ # set shunts
                'logic' : "(ra1 < 1.0) or (ra2 < -26)",
                'actTime' : 30, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04) or (ra2 > 26)",
                'actTime' : 30, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 90, # minimum time between actions
            }, # end timers
        },# end bus8caps
    'bus9caps' : {
        'RefAgents' : {
            'ra1' : 'bus 9 : Vm',
            'ra2' : 'branch 8 9 1 : Qbr', # branches defined from, to, ckID
            },# end Referenc Agents
        'TarAgents' : {
            'tar1' : 'shunt 9 2 : St',
            'tar2' : 'shunt 9 3 : St',
            'tar3' : 'shunt 9 4 : St',
            'tar4' : 'shunt 9 5 : St',
            'tar5' : 'shunt 9 6 : St',
            }, # end Target Agents
        'Timers' : {
            'set' :{ # set shunts
                'logic' : "(ra1 < 1.0) or (ra2 > 13.3)",
                'actTime' : 80, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04) or (ra2 < -13.3)",
                'actTime' : 80, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 120, # minimum time between actions
            }, # end timers
        },# end bus8caps
    }# end DTCdict

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
            "gen 4 : 1.0", 
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

"""