def cleanLtdStr(inStr):
    """Parse ltd string into list of more easily workable parts
    Removes any comments and casts most common parameters
    """
    #print("dirty: %s" % inStr)
    clean = []
    a = inStr.split(":")
    b = a[0].split()
    c = a[1].split()

    clean.append(b[0])                  # 
    clean.append(float(b[1]))             # busnum / area num
    if len(b) > 2:
        clean.append(b[2])              # Id (if available)
    else:
        clean.append(None)

    for n in range(len(c)):
        # ignore inline comments
        if '"' in c[n]:
            continue

        clean.append(c[n])

    #print("clean: %s" % clean)
    """ 
    # debug
    for x in range(len(clean)):
        print(x, clean[x], type(clean[x]))
    print(len(clean))
    """
    return clean