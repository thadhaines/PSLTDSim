"""Script adds objects to __builtin__ for true globals"""

import __builtin__

# __builtin__ used to create truly global objects (enables interactive mode to work)

# CoreAgents
__builtin__.AreaAgent = AreaAgent
__builtin__.BusAgent = BusAgent
__builtin__.GeneratorAgent = GeneratorAgent
__builtin__.SlackAgent = SlackAgent
__builtin__.LoadAgent = LoadAgent

# Loose Functions
__builtin__.parseDyd = parseDyd
__builtin__.distPe = distPe
__builtin__.combinedSwing = combinedSwing
__builtin__.saveMirror = saveMirror

# FindFunctions
__builtin__.findLoadOnBus = findLoadOnBus
__builtin__.findGenOnBus = findGenOnBus

#PertrubanceAgents
__builtin__.LoadStepAgent = LoadStepAgent