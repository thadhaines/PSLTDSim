def getCurrentVal(agent, attr):
    """Handle getting the most recent agent value for a number of attributes"""
    if attr == 'p':
        #load power
        return agent.P
    elif attr == 'q':
        #load q
        return agent.Q
    elif attr == 'pset':
        #governed generator Pset
        return agent.Pset
    elif attr == 'pm':
        #un-governed generator Pm
        return agent.Pm
    else:
        print('* * Attribute not found in Agent...') # shouldn't ever print