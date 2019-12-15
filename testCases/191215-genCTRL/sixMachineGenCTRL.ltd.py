# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored


# Perturbances
mirror.sysPerturbances = [
    #'load 9 : ramp P 2 40 10 per',
    ]

#mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 0.03, True)
mirror.sysGenerationControl = {
    'testSystem' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : 10,
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