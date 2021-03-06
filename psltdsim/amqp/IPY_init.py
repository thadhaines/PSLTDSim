def IPY_init(msg):
    """Handle PY3 init message
    Set locations and simParams as true globals"""
    import __builtin__

    __builtin__.locations = msg['locations']
    __builtin__.simParams = msg['simParams']
    __builtin__.simNotes = msg['simNotes']
    __builtin__.debug = msg['debug']
    __builtin__.AMQPdebug = msg['AMQPdebug']
    __builtin__.debugTimer = msg['debugTimer']