def PY3importMir(msg):
    """ handle import of mirror from msg location"""
    import builtins
    mir = ltd.data.readMirror(msg['mirLoc'])
    builtins.mir = mir
    return