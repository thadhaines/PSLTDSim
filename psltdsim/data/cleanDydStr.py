def cleanDydStr(str):
    """Parse dyd string into list of more easily workable parts
    Removes any comments and casts most common parameters 
    Assumes busnum is int, all parameters after #X or mXX= are floats
    """
    clean = []
    a = str.split(":")
    b = a[0].split('"')
    c = str.split()
    d = a[1].split()
 
    clean.append(c[0])                  # model
    clean.append(int(c[1]))             # busnum
    clean.append(b[1].rstrip())         # busnam
    clean.append(float(b[2].strip()))   # base kV
    clean.append(b[3].strip())          # id?

    for n in range(len(d)):
        #set IMPORT = 0.0
        if (d[n] == 'IMPORT'):
            d[n] = 0.0
            clean.append(d[n])
            continue

        # not cast # identifier
        if '#' in d[n]:
            clean.append(d[n])
            continue

        # ignore inline comments
        if '"' in d[n]:
            continue

        # parse value from mva= 
        # funtionality removed - may cause confusion if not defined.
        if '=' in d[n]:
            #e = d[n].split('=')
            #clean.append(float(e[1]))
            clean.append(d[n])
            continue
        
        clean.append(float(d[n]))

    """ 
    # debug
    for x in range(len(clean)):
        print(x, clean[x], type(clean[x]))
    print(len(clean))
    """
    return clean