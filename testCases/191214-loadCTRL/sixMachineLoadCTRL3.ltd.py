# LTD simulation models / perturbances
# Attribute name case sensitive.
# Commented and empty lines are ignored during parsing.
# Double quoted variable names in model parameters also ignored


# Perturbances
mirror.sysPerturbances = [
    'load 9 : step P 225 100 rel',
    ]

mirror.NoiseAgent = ltd.perturbance.LoadNoiseAgent(mirror, 1.0 , True)

mirror.sysLoadControl = {
    'testSystem' : {
        'Area': 2,
        'startTime' : 2,
        'timeScale' : 10,
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