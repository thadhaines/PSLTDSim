import datetime

def getTimeStr():
    """Return Time String"""
    return datetime.datetime.now().strftime('%H:%M:%S.%f')