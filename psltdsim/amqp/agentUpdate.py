def agentUpdate(mirror, msg):
    """Sends agent update messages to correct mirror agent function"""
    tarType = msg['AgentType']

    if tarType == 'Generator':
        target = ltd.find.findGenOnBus(mirror, msg['Busnum'],msg['Id'])

    elif tarType == 'Bus':
        target = ltd.find.findBus(mirror, msg['Extnum'])

    elif tarType == 'Load':
        target = ltd.find.findLoadOnBus(mirror, msg['Busnum'],msg['Id'])

    else:
        print("Unrecognized Target Type: %s" % tarType)
        return

    if target:
        # target found, pass message
        target.recAMQPmsg(msg)
        return
    else:
        print("Message target not found, message lost:")
        print(msg)