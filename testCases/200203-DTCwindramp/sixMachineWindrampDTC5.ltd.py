# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

CTRLtimeScale = 60*60 # ninutes
ACEgain = 16.0

# Perturbances
mirror.sysPerturbances = [
    # ramp non-gov gens
    'gen 2 2 : ramp Pm 300 2700 150 rel', # 45 min ramp up
    'gen 2 2 : ramp Pm 3600 2700 -150 rel', # 45 min ramp down
    'gen 5 : ramp Pm 300 2700 300 rel', # 45 min ramp up
    'gen 5 : ramp Pm 3600 2700 -300 rel', # 45 min ramp down
    'mirror : ramp Hsys 300 2700 -20 per', # 45 min ramp down
    'mirror : ramp Hsys 3600 2700 25 per', # 45 min ramp up
    # ramp loads
    #'load 8 : ramp P 600 2700 150 rel', # 45 min ramp up
    #'load 8 : ramp P 3900 2700 -150 rel', # 45 min ramp down
    #'load 9 : ramp P 600 2700 300 rel', # 45 min ramp up
    #'load 9 : ramp P 3900 2700 -300 rel', # 45 min ramp down
    ]

mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True, 5) # mirror, percent noise, walk, delay@ start

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
                'logic' : "(ra1 < 1.0)",
                'actTime' : 30, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04)",
                'actTime' : 30, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 60, # minimum time between actions
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
                'logic' : "(ra1 < 1.0)",
                'actTime' : 80, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04)",
                'actTime' : 80, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 120, # minimum time between actions
            }, # end timers
        },# end bus9caps
    }# end DTCdict

# Balancing Authorities
mirror.sysBA = {
    'BA1':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 300, # seconds 
        'ACEgain' : ACEgain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'ramp', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': ['gen 1 : 0.5 : rampA',
                     'gen 2 1 : 0.5 : rampA',
                     ]
        },
    'BA2':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 300.00, # seconds 
        'ACEgain' : ACEgain,
        'AGCType':'TLB : 0', # Tie-Line Bias 
        'UseAreaDroop' : False,
        'AreaDroop' : 0.05,
        'IncludeIACE' : True,
        'IACEconditional': False,
        'IACEwindow' : 30, # seconds - size of window - 0 for non window
        'IACEscale' : 1/15,
        'IACEdeadband' : 0, # Hz 
        'ACEFiltering': 'PI : 0.04 0.0001', 
        'AGCDeadband' : None, # MW? -> not implemented
        'GovDeadbandType' : 'ramp', # step, None, ramp, nldroop
        'GovDeadband' : .036, # Hz
        'GovAlpha' : 0.016, # Hz - for nldroop
        'GovBeta' : 0.036, # Hz - for nldroop
        'CtrlGens': ['gen 3 : 0.6 : rampA',
                     'gen 4 : .4 : rampA',
                     ]
        },
    }

# Load and Generation Cycle Agents
"""
mirror.sysGenerationControl = {
    'BPATDispatch' : {
        'Area': 1,
        'startTime' : 2,
        'timeScale' : CTRLtimeScale,
        'rampType' : 'per', # relative percent change
        'CtrlGens': [
            "gen 1 : 0.25",
            "gen 2 1 : 0.75", 
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