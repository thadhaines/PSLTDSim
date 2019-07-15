def findPowerPlant(mirror, name):
    """Return power plant agent, if it exists"""
    if name in mirror.ppDict:
        return mirror.ppDict[name]
    else:
        print("*** Power Plant '%s' not found." % name)
        return None