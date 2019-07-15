# added processing time seems not worth added 'accuracy'
def single2float(x):
    """Convert a single x to a rounded floating point number
    that has the same number of decimals as the original"""
    dPlaces = len(str(x).split('.')[1])
    y = round(float(x),dPlaces+2)

    # NOTE: Alternative method:
    #y = round(float(x),6)
    return y
