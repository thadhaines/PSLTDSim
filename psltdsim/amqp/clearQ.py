import pika 

def clearQ(host, queues):
    """Clear any messages in the queues of given host
    queues may be a list or single string
    """

    cParams = pika.ConnectionParameters(host=host)
    connection = pika.BlockingConnection(cParams)
    channel = connection.channel()

    if type(queues) == 'str': # prevent extra iterations
        queues = [queues]

    for q in queues:
        channel.queue_purge(q)
        #print('purged %s' % q) # Debug

    connection.close()