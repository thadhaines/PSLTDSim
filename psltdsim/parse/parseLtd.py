def parseLtd(mirror,ltdLoc):
    """Function that parses ltd information to mirror"""
    
    totPertfound = 0
    for ltdFileNdx in range(len(ltdLoc)): # assumes ltd in list, will handle multiples
        file = open(ltdLoc[ltdFileNdx], 'r') # open file to read
        if mirror.debug: print("*** Parsing LTD file at %s" % ltdLoc[ltdFileNdx])
        line = next(file) # get first line of file
        foundPert = 0

        while line:
            if line[0] == '#' or line[0] =='\n':
                    # line blank or comment, skip
                    line = next(file, None)
                    continue

            #print(line) # Debug
            parts = line.split()

            # send line to correct function based on line
            if parts[0] == "load":
                if mirror.debug:
                    print("*** Creating %s Perturbance..." % parts[0])
                cleanLine = ltd.parse.cleanLtdStr(line)

                # turn clean line into idList
                if cleanLine[2]:
                    idList = cleanLine[1:3]
                else:
                    idList = [cleanLine[1]]

                ltd.mirror.addPerturbance(mirror, 
                                          cleanLine[0],
                                         idList,
                                         cleanLine[3],
                                         cleanLine[4:])

                #print(line) # debug

                foundPert += 1
  
            line = next(file,  None) # get next line, if there is one

        file.close() # close file
        totPertfound += foundPert
    if mirror.debug == 1:
        print("*** Parsed %d perturbances from:\n%s" 
              % (totPertfound, ltdLoc))