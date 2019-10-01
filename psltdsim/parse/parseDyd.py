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

    # Creation of Model dictionaries Hlocation and Dloc for each gen type +6
    unModeledPSLFmachines = {
        'genrou' :  {'Hloc' : 11, 'Dloc' : 12 },
        'gencc' :   {'Hloc' : 11, 'Dloc' : 12 },
        'gencls' :  {'Hloc' : 7, 'Dloc' : 8 },
        'genind ' : {'Hloc' : 11, 'Dloc' : 12 },
        'gensal' :  {'Hloc' : 10, 'Dloc' : 11 },
        'gensdo' :  {'Hloc' : 9, 'Dloc' : 10 },
        'gentpf' :  {'Hloc' : 11, 'Dloc' : 12 },
        'gentpj' :  {'Hloc' : 11, 'Dloc' : 12 },
        'genwri' :  {'Hloc' : 12, 'Dloc' : 13 },
        'gewtg' :   {'Hloc' : 1, 'Dloc' : 1 }, # has no inertia or damping - Wind turbine
        'motor1' :  {'Hloc' : 11, 'Dloc' : 12 },
        'motorc' :  {'Hloc' : 1, 'Dloc' : 1 }, # eperimental model - not supported by GE....? no info given
        'motorw' :  {'Hloc' : 12, 'Dloc' : 6 },
        'motorx' :  {'Hloc' : 15, 'Dloc' : 16 },
        'shaft5' :  {'Hloc' : 8, 'Dloc' : 12 }, # Call GE for details...
       }

    unModeledPSLFprimeMovers = {
        'model name': {'TurbineType': 'unknown', 'Rloc' : 6, 'Hloc' : 8, 'Mbase' : 2 , 'MWcap' : 0,}, # Generic Data Line for gov info, rloc +6
        'tgov1':   {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, # droop as first param, damping as last (7th)
        'ccbt1' :  {'LTDTurbineType': 'steam', 'Rloc' : 8, 'Dloc' : 'Not Listed',}, # rvalve 2
        'ccst3' :  {'LTDTurbineType': 'steam', 'Rloc' : 15, 'Dloc' : 'Not Listed',},  # r 8
        'crcmgv' : {'LTDTurbineType': 'steam', 'Rloc' : 8, 'Dloc' : 14,}, #HP droop, has 2
        'degov1' : {'LTDTurbineType': 'diesel', 'Rloc' : 17, 'Dloc' : 'Not Listed',}, 
        'g2wscc' : {'LTDTurbineType': 'hydro', 'Rloc' : 9, 'Dloc' : 'Not Listed',}, 
        'gast' :   {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 10,}, # damping not used, single shaft turbine
        'gegt1' :  {'LTDTurbineType': 'gas', 'Rloc' : 8, 'Dloc' : 13,}, # Hz per MW droop..., has deadband listing in PU
        'ggov1' :  {'LTDTurbineType': 'general', 'Rloc' : 7, 'Dloc' : 29,}, # GENERAL
        'ggov2' :  {'LTDTurbineType': 'general', 'Rloc' : 7, 'Dloc' : 29,}, 
        'ggov3' :  {'LTDTurbineType': 'general', 'Rloc' : 7, 'Dloc' : 29,}, 
        'gpwscc' : {'LTDTurbineType': '_', 'Rloc' : 9, 'Dloc' : 'Not Listed',}, # 2 deadbands listed
        'h6b' :    {'LTDTurbineType': 'hydro', 'Rloc' : 'Not Listed', 'Dloc' : 'Not Listed',}, # no droop listed?

        'h6bd' :   {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hyg3' :   {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hygov4' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hygov8' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hygov' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hygovr' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hypid' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'hyst1' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'ieeeg1' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'ieeeg3' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'lcfb1' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'lm2500' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'lm6000' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'pidgov' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'stag1' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'tgov1' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'tgov3' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'w2301' :  {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'wndtge' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
        'wndtrb' : {'LTDTurbineType': 'steam', 'Rloc' : 7, 'Dloc' : 13,}, 
       }


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

            # Check if parts[0] in unmodeled dict for gen or prime mover
            if parts[0] in unModeledPSLFmachines:
                if mirror.debug:
                        print("*** Creating Generic Machine info for bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.genericMachine(mirror, cleanLine, unModeledPSLFmachines[parts[0]])
                mirror.PSLFmach.append(newPmod)
                foundPModels += 1

            if parts[0] in unModeledPSLFprimeMovers:
                if mirror.debug:
                        print("*** Creating Generic Prime Mover info for bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.genericPrimeMover(mirror, cleanLine, unModeledPSLFprimeMovers[parts[0]])
                mirror.PSLFmach.append(newPmod)
                foundPModels += 1
            
            """ commented out for debug of generic machine functionality
            if parts[0] == "genrou":
                if mirror.debug:
                    print("*** Creating genrou on bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.genrou(mirror, cleanLine)
                mirror.PSLFmach.append(newPmod)
                foundPModels += 1
            """

            if parts[0] == "tgov1":
                if mirror.debug:
                    print("*** Creating tgov1 info for bus %s..." % parts[1])
                cleanLine = ltd.parse.cleanDydStr(line)
                newPmod = ltd.pslfModels.tgov1(mirror, cleanLine)
                mirror.PSLFgov.append(newPmod)
                foundPModels += 1

            # LTD Models (proof of concept) - Will probably be removed
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