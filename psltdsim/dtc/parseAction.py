def parseAction(DTCAgent, operation, actionSTR):
    """ parse action string, return populated string for execution
    Doesn't account for 'bad input' references / targets
    """
    debug = DTCAgent.mirror.debug

    # seperate act input string post operation
    opSize = len(operation)
    for ndx, val in enumerate(actionSTR):

        if val == operation[0]:
            actStart = ndx+opSize
            break

    act = actionSTR[actStart:]

    # list of tuples for location and name of references/targets
    foundNdx = []

    #enumerate for parse/link action
    for ndx, val in enumerate(act):
        #print(ndx, val) # DEBUG

        # Target var check
        if val.lower() == 't':
            aCheck = act[ndx+1].lower() == 'a'
            rCheck = act[ndx+2].lower() == 'r'
            digitCheck = act[ndx+3].isdigit()
            try:
                digitCheck2 = act[ndx+4].isdigit() # possible double digit
            except IndexError: # for action ending in tar/ra single digit
                digitCheck2 = False
        
            if all([aCheck,rCheck,digitCheck]):
                if digitCheck2:
                    endNdx = ndx+5
                    if debug:
                        print('Tar found: loc %d:%d'% (ndx,endNdx)) #DEBUG
                else:
                    endNdx = ndx+4
                    if debug:
                        print('Tar found: loc %d:%d'% (ndx,endNdx)) #DEBUG

                # index found, check if in tar dic
                if act[ndx:endNdx] in DTCAgent.tar:
                    if debug:
                        print('Target %s points to %s' %
                          (act[ndx:endNdx], DTCAgent.tar[act[ndx:endNdx]])) #DEBUG
                    # create list of tuples for replace vals
                    foundNdx.append((act[ndx:endNdx],ndx,endNdx))

        # Reference var check
        if val.lower() == 'r':
            #possible begining of tar variable
            aCheck = act[ndx+1].lower() == 'a'
            digitCheck = act[ndx+2].isdigit()

            try:
                digitCheck2 = act[ndx+3].isdigit() # possible double digit
            except IndexError:
                digitCheck2 = False

            if all([aCheck,digitCheck]):
                if digitCheck2:
                    endNdx = ndx+4
                    if debug:
                        print('Ra found: loc %d:%d'% (ndx,endNdx)) #DEBUG
                else:
                    endNdx = ndx+3
                    if debug:
                        print('Ra found: loc %d:%d'% (ndx,endNdx)) #DEBUG

                # index found, check if in tar dic
                if act[ndx:endNdx] in DTCAgent.ra:
                    if debug:
                        print('Reference %s points to %s' %
                          (act[ndx:endNdx], DTCAgent.ra[act[ndx:endNdx]])) #DEBUG
                    # create list of tuples for replace vals
                    foundNdx.append((act[ndx:endNdx],ndx,endNdx))


    # Found index tuple list foundNdx built, build new string....
    #blank string
    newAct = ''
    refEnd = 0

    for tup in foundNdx:
        # Handle assigning index according to foundNdx values
        refStart = tup[1]
        newAct+= act[refEnd:refStart]
        refEnd = tup[2]
    
        # check for targets
        if tup[0][0] == 't':
            # put target value into string
            newAct += DTCAgent.tar[tup[0]].getNewAttrSTR()

        #check for references
        if tup[0][0] == 'r':
            # put reference value into string
            newAct += DTCAgent.ra[tup[0]].getNewAttrSTR()

    # account for any post reference action
    newAct+= act[refEnd:]
    print("input str : %s" % act)
    print("output str: %s" % newAct)

    return newAct

