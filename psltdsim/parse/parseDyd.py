"""Functions to parse dyd file information to python mirror
Assumes each valid dyd line is a separate dynamic element of the form:
genrou 12 "GRANDC-G3   " 20.00  "1 "  : #9 mva=9000.0000 6.0000 0.0250 0.0600 0.0400 5.0000 0.0000 1.2000 0.7000 0.3000 0.2300 0.2200 0.1700 0.0500 0.3000 0.0000 0.0000 0.0000 0.0000
"""

def parseDyd(mirror,dydLoc):
    """Function that parses dyd information to mirror PSLFdyanmics list
    Will parse particular dyd models to intermediate classes
    these classes will be referenced by the model to populate dynamic properties
    """

    totFPmodels = 0
    totFLTDmodels = 0

    # TODO: enable multi dyd overwrite
    for dyd in range(len(dydLoc)): #-> dydLoc is then replaced with dydLoc[dyd]
        file = open(dydLoc[dyd], 'r') # open file to read
        if mirror.debug: print("*** Parsing dynamics file at %s" % dydLoc[dyd])
        line = next(file) # get first line of file
        foundPModels = 0
        foundLTDModels = 0
        cline = None # used in continued line operation

        while line:
            if line[0] == '#' or line[0] =='\n':
                # ignore comments and blanks
                line = next(file, None)
                continue
            
            if cline:
                # handle slash removal and string concatonation
                line = cline[:-1]+line
                cline = None

            #print(line) # Debug
            parts = line.split()

            if parts[-1] == '/':
                # save continued line, get next line
                cline = line
                line = next(file, None)
                continue

            cline = None # line complete

            if parts[0] == "genrou":
                if mirror.debug:
                    print("*** Creating genrou on bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.genrou(mirror, cleanLine)
                mirror.PSLFmach.append(newPmod)
                foundPModels += 1

            if parts[0] == "tgov1":
                if mirror.debug:
                    print("*** Creating tgov1 on bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.tgov1(mirror, cleanLine)
                mirror.PSLFgov.append(newPmod)
                foundPModels += 1

            if parts[0] == "ggov1":
                if mirror.debug:
                    print("*** Creating ggov1 on bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.ggov1(mirror, cleanLine)
                mirror.PSLFgov.append(newPmod)
                foundPModels += 1

            # LTD Models (proof of concept)
            if parts[0] == "pgov1":
                cleanLine = ltd.parse.cleanDydStr(line)
                newLTDmod = ltd.dynamicAgents.pgov1Agent(mirror, cleanLine)

                # create refereces to agent in Generator and model
                newLTDmod.Gen.gov.append(newLTDmod)
                mirror.Dynamics.append(newLTDmod)
                #print(line) # for debug
                foundLTDModels += 1
  
            line = next(file,  None) # get next line, if there is one

        file.close() # close file
        totFPmodels += foundPModels
        totFLTDmodels += foundLTDModels
    if mirror.debug == 1:
        print("*** Parsed %d PSLF models and %d LTD models from:\n%s" 
              % (totFPmodels,totFLTDmodels, dydLoc))