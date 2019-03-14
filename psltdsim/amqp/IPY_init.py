def IPY_init(msg):
    """Handle PY3 init message
    Essentially set locations and simParams as true globals"""
    import __builtin__

    __builtin__.locations = msg['locations']
    __builtin__.simParams = msg['simParams']
