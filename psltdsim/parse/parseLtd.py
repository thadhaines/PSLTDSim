def parseLtd(mirror,ltdList):
    """Function that parses sysPert list information to mirror"""
    
    totPertfound = 0
    for ltdEntry in ltdList: # assumes ltd in list, will handle multiples
        
        foundPert = 0

        #print(line) # Debug
        parts = ltdEntry.split()

        t = parts[0].lower()# for shorter logic comparisons

        # send line to correct function based on line
        if (t == "load") or (t =="gen") or (t =="shunt"):
            if mirror.debug:
                print("*** Creating %s Perturbance..." % parts[0])
            cleanLine = ltd.parse.cleanLtdStr(ltdEntry)

            # turn clean line into idList
            if cleanLine[2]:
                idList = cleanLine[1:3]
            else:
                idList = [cleanLine[1]]

            ltd.perturbance.addPerturbance(mirror, 
                                        cleanLine[0],
                                        idList,
                                        cleanLine[3],
                                        cleanLine[4:])

        elif t == "branch":
            if mirror.debug:
                print("*** Creating %s Perturbance..." % parts[0])
            cleanLine = ltd.parse.cleanLtdStr(ltdEntry)

            # turn clean line into idList
            idList = cleanLine[1:4]

            ltd.perturbance.addPerturbance(mirror, 
                                        cleanLine[0],
                                        idList,
                                        cleanLine[4],
                                        cleanLine[5:])
            #print(line) # debug

            foundPert += 1

        totPertfound += foundPert

    if mirror.debug == 1:
        print("*** Parsed %d perturbances from:\n%s" 
              % (totPertfound, ltdList))