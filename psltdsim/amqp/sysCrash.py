def sysCrash(mirror):
    """Handle ending simulation via AMQP sysCrash message"""
    mirror.sysCrash = True
    mirror.N = mirror.cv['dp']