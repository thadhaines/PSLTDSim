# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
mirror.sysPerturbances = [
    # Init step for dtc testing
    'load 8 : step P 4 250 rel',
    'load 8 : step P 30 250 rel',
    'load 8 : step P 60 -500 rel',
    'load 8 : step P 90 -250 rel',
    # ramp non-gov gens
    'gen 2 2 : ramp Pm 600 2700 150 rel', # 45 min ramp up
    'gen 2 2 : ramp Pm 3900 2700 -150 rel', # 45 min ramp down
    'gen 5 : ramp Pm 600 2700 300 rel', # 45 min ramp up
    'gen 5 : ramp Pm 3900 2700 -300 rel', # 45 min ramp down
    # ramp loads
    'load 8 : ramp P 600 2700 150 rel', # 45 min ramp up
    'load 8 : ramp P 3900 2700 -150 rel', # 45 min ramp down
    'load 9 : ramp P 600 2700 300 rel', # 45 min ramp up
    'load 9 : ramp P 3900 2700 -300 rel', # 45 min ramp down
    ]
#mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True)

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
                'logic' : "(ra1 < 1.0) or (ra2 < -25)",
                'actTime' : 5, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04) or (ra2 > 35)",
                'actTime' : 3, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 10, # minimum time between actions
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
                'logic' : "(ra1 < 1.0) or (ra2 > 25)",
                'actTime' : 9, # seconds of true logic before act
                'act' : "anyOFFTar = 1", # set any target off target = 1
            },# end set
            'reset' :{ # reset shunts
                'logic' : "(ra1 > 1.04) or (ra2 < -30)",
                'actTime' : 8, # seconds of true logic before act
                'act' : "anyONTar = 0", # set any target On target = 0
            },# end reset
            'hold' : 10, # minimum time between actions
            }, # end timers
        },# end bus8caps
    }# end DTCdict


# Balancing Authorities
mirror.sysBA = {
    'BA1-BPAT':{
        'Area':1,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 30.00, # seconds 
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
        'CtrlGens': ['gen 1 : 0.5 : rampA',
                     'gen 2 1 : 0.5 : rampA',
                     ]
        },
    'BA2-CAISO':{
        'Area':2,
        'B': "1.0 : perload", # MW/0.1 Hz
        'AGCActionTime': 45.00, # seconds 
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
