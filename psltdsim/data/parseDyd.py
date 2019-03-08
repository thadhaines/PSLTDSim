"""Functions to parse dyd file information to python mirror
Assumes each valid dyd line is a separate dynamic element of the form:
genrou 12 "GRANDC-G3   " 20.00  "1 "  : #9 mva=9000.0000 6.0000 0.0250 0.0600 0.0400 5.0000 0.0000 1.2000 0.7000 0.3000 0.2300 0.2200 0.1700 0.0500 0.3000 0.0000 0.0000 0.0000 0.0000
"""

#import PSLF_model_templates as pmod

def parseDyd(model,dydLoc):
    """Function that parses dyd information to mirror PSLFdyanmics list
    Will parse particular dyd models to intermediate classes
    these classes will be referenced by the model to populate dynamic properties
    """
    #import __builtin__
    if model.debug: print("*** Parsing file at %s" % dydLoc)

    # TODO: enable multi dyd overwrite
    for dyd in range(len(dydLoc)): #-> dydLoc is then replaced with dydLoc[dyd]
        file = open(dydLoc[dyd], 'r') # open file to read
        line = next(file) # get first line of file
        foundPModels = 0
        foundLTDModels = 0

        while line:
            if line[0] == '#' or line[0] =='\n':

                if line[0] == '\n':
                    # line blank, skip
                    line = next(file, None)
                    continue

                if line[1] == '!':
                    # line is a custom LTD model, remove shebang and parse
                    line = line[2:]
                    
                else:
                    # line is a comment
                    line = next(file, None)
                    continue

            #print(line) # Debug
            parts = line.split()
        
            if parts[0] == "genrou":
                if model.debug:
                    print("Creating genrou on bus %s..." % parts[1])
                cleanLine = ltd.data.cleanDydStr(line)
                newPmod = ltd.pslfModels.genrou(model, cleanLine)
                model.PSLFmach.append(newPmod)
                foundPModels += 1

            # LTD Models (proof of concept)
            if parts[0] == "pgov1":
                cleanLine = ltd.data.cleanDydStr(line)
                newLTDmod = ltd.dynamicAgents.pgov1Agent(model, cleanLine)

                # create refereces to agent in Generator and model
                newLTDmod.Gen.gov.append(newLTDmod)
                model.Dynamics.append(newLTDmod)
                print(line) # for debug
                foundLTDModels += 1
  
            line = next(file,  None) # get next line, if there is one

        file.close() # close file

    if model.debug == 1:
        print("Parsed %d models from dyd:  %s" % (foundPModels, dydLoc))