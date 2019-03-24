def PY3importMir(msg):
    """ handle import of mirror from msg location
    Try except used to handle file closure handoff issues"""
    import builtins
    import time

    unfinished = True
    while unfinished:
        try:
            mir = ltd.data.readMirror(msg['mirLoc'])
            unfinished = False
        except:
            time.sleep(0.001)
            print('Slept 0.001 sec waiting for mirror....') # to see what the deal is...

    builtins.mir = mir
    return