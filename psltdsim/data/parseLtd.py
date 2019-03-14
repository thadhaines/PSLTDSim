def parseLtd(model,ltdLoc):
    """Function that parses ltd information to mirror"""

    totPertfound = 0
    for ltd in range(len(ltdLoc)): # assumes ltd in list, will handle multiples
        file = open(ltdLoc[ltd], 'r') # open file to read
        if model.debug: print("*** Parsing file at %s" % ltdLoc[ltd])
        line = next(file) # get first line of file
        foundPert = 0

        while line:
            if line[0] == '#' or line[0] =='\n':
                    # line blank or comment, skip
                    line = next(file, None)
                    continue

            print(line) # Debug
            parts = line.split()
        
            if parts[0] == "load":

                if model.debug:
                    print("*** Creating DEBUG on  %s..." % parts[0])
                #cleanLine = ltd.data.cleanDydStr(line)
                print(line)
                foundPert += 1
  
            line = next(file,  None) # get next line, if there is one

        file.close() # close file
        totPertfound += foundPert
    if model.debug == 1:
        print("*** Parsed %d perturbances from:\n%s" 
              % (totPertfound, ltdLoc))