import datetime

def getTimestr():
    """Return Time String"""
    return datetime.datetime.now().strftime('%H:%M:%S.%f')