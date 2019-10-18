def pdif(val1, val2):
    """Calculate absolute percent difference between val1 and val2"""
    ave = abs((val1+val2)/2.0)
    dif = abs(val1-val2)
    return dif/ave*100
