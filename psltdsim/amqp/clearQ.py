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
        try:
            channel.queue_purge(q)
        except:
            print('*** AMQP queues do not exist - nothing to purge.')
        #print('purged %s' % q) # Debug

    connection.close()