def getCurrentVal(agent, attr):
    """Handle getting the most recent agent value for a number of attributes"""

    if attr in agent.cv:
        return agent.cv[attr]
    else:
        print('* * Attribute ''%s'' not found in Agent...' % attr) # shouldn't ever print