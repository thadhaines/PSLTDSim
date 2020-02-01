# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored

# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 2 20 per', # step load up 20%
    'load 8 : step P 10 20 per', # step load up 20%
    'load 8 : step P 30 600 abs', # step load to 600 MW
    'load 9 : ramp P 24 15 -600 rel',
    ]

mirror.ShuntControl = {
    'bus8Caps' : {
        'RefAgentType' : 'bus',
        'RefAgentID' : '8',
        'SetLogic' : 'Vm : <0.95',
        'SetTime' : 3, # seconds
        'SetCountType' : 'abs', # Type of counter to trigger
        'ResetLogic' : 'Vm : >1.05',
        'ResetTime' : 5, # seconds
        'ResetCountType' : 'per : .9',
        'HoldTime' : 0, # seconds, minimum time between actions
        'CtrlShunts' : [
            "shunt 8 2",
            "shunt 8 3",
            "shunt 8 4",
            "shunt 8 5",
            ],
        },# end agend def
    'bus9Caps' : {
        'RefAgentType' : 'bus',
        'RefAgentID' : '9',
        'SetLogic' : 'Vm : <0.95',
        'SetTime' : 5, # seconds
        'SetCountType' : 'abs', # Type of counter to trigger
        'ResetLogic' : 'Vm : >1.05',
        'ResetTime' : 5, # seconds
        'ResetCountType' : 'per : .9',
        'HoldTime' : 0, # seconds, minimum time between actions
        'CtrlShunts' : [
            "shunt 9 2",
            "shunt 9 3",
            "shunt 9 4",
            "shunt 9 5",
            ],
        }, # end agent def
    }# end agents def



#mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True)
"""
mirror.sysGenerationControl = {
    'testSystem' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : 15,
        'rampType' : 'per', # relative percent change
        'CtrlGens': [
            "gen 3 : 1.0",
            #"gen 3 : 0.5", 
            #"gen 4 : 0.5",
            ],
        # Data from: 12/11/2019 PACE
        'forcast' : [ 
            #(time , Precent change from previous value)
            (0, 0.000),
            (1, 5.137),
            (2, 6.098),
            (3, 4.471),
            (4, 1.110),
            (5, -1.018),
            (6, -1.254),
            (7, -1.205),
            (8, -1.104),
            (9, -0.866),
            (10, -0.521),
            (11, 0.524),
            (12, 3.563),
            (13, 3.927),
            (14, 1.530),
            (15, -1.092),
            (16, -1.695),
            (17, -2.926),
            (18, -4.709),
            (19, -4.429),
            (20, -3.382),
            (21, -2.389),
            (22, -1.157),
            (23, 0.077),
            (24, 1.764),
            (25, 4.429),
            (26, 6.389),
            (27, 4.936),
            (28, 1.600),
            (29, -0.573),
            (30, -0.944),
            (31, -1.050),
            (32, -0.947),
            (33, -0.758),
            ],
        }, #end of generation controller def
    }


mirror.sysLoadControl = {
    'testSystem' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : 15,
        'rampType' : 'per', # relative percent change
        # Data from: 12/11/2019 PACE
        'demand' : [ 
            #(time , Precent change from previous value)
            (0, 0.000),
            (1, 3.675),
            (2, 6.474),
            (3, 3.770),
            (4, -2.095),
            (5, 0.184),
            (6, 1.769),
            (7, 0.262),
            (8, -0.458),
            (9, 0.049),
            (10, -0.837),
            (11, 1.689),
            (12, 2.410),
            (13, 4.007),
            (14, -0.780),
            (15, -0.431),
            (16, -2.414),
            (17, -2.062),
            (18, -6.736),
            (19, -5.156),
            (20, -3.075),
            (21, -2.531),
            (22, -0.271),
            (23, -0.369),
            (24, 0.468),
            (25, 3.436),
            (26, 7.281),
            (27, 5.317),
            (28, -3.969),
            (29, 2.421),
            (30, 2.533),
            (31, -1.169),
            (32, 0.867),
            (33, -0.611),
        ] ,
                },# end of demand load control definition
}
"""
