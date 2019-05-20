def PY3importMir(msg):
    """ handle import of mirror from msg location
    Try except used to handle file closure handoff issues"""
    import builtins
    import time

    unfinished = True
    rTime = 0.0
    while unfinished:
        try:
            mir = ltd.data.readMirror(msg['mirLoc'])
            unfinished = False
        except BaseException as e:
            print(e)
            time.sleep(0.001)
            rTime += 0.001
            print('Slept %.3f sec waiting for mirror....' % rTime) # to see what the deal is...

    builtins.mir = mir
    return