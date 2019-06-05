def getCurrentVal(agent, attr):
    """Handle getting the most recent agent value from cv dictionary"""

    if attr in agent.cv:
        return agent.cv[attr]
    else:
        print('*** Attribute \'%s\' not found in Agent...' % attr) 
        return None