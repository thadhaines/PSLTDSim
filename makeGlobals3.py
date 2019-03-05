"""Script adds objects to builtins for true globals"""

import builtins

# builtins used to create truly global objects (enables interactive mode to work)

# CoreAgents
builtins.AreaAgent = AreaAgent
builtins.BusAgent = BusAgent
builtins.GeneratorAgent = GeneratorAgent
builtins.SlackAgent = SlackAgent
builtins.LoadAgent = LoadAgent

# Loose Functions
builtins.parseDyd = parseDyd
builtins.distPe = distPe
builtins.combinedSwing = combinedSwing

# FindFunctions
builtins.findLoadOnBus = findLoadOnBus
builtins.findGenOnBus = findGenOnBus

#PertrubanceAgents
builtins.LoadStepAgent = LoadStepAgent

# Dynamic Agents
builtins.pgov1Agent = pgov1Agent