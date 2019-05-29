def makeGroupMsg(group):
    """ create a list of dictionary messages"""
    # not used
    N = len(group)
    groupMsg = [0.0]*N
    ndx = 0
    for member in group:
        groupMsg[ndx] = member.makeAMQPmsg()
        # vary group size here
        ndx+=1

    return groupMsg
