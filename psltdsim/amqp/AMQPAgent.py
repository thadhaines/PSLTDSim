import json
import pika
import datetime

class AMQPAgent():
    """Can send and receive msgs, init with host string and msg format
        uses json dumps and loads to send/receive native python objects"""
    def __init__(self, name, host, mirror=None):
        self.name = name
        self.host = host
        self.mirror = mirror

    def send(self,msgQueue,msg):
        """send msg to msgQueue"""
        cParams = pika.ConnectionParameters(host=self.host)
        connection = pika.BlockingConnection(cParams)
        channel = connection.channel()
        channel.queue_declare(queue=msgQueue) # ensure queue created

        if self.mirror:
            if self.mirror.AMQPdebug:
                print(datetime.datetime.now().strftime('%H:%M:%S.%f') +
                 ' ' + self.name + " Sending \t %r" % json.dumps(msg))
        
        channel.basic_publish(exchange='', 
                              routing_key=msgQueue, 
                              body=json.dumps(msg) )
        connection.close()

    def debugCallback(self, ch, method, properties, body):
        """should be altered to specific needs - proof of concept shown"""
        if self.mirror:
            if self.mirror.AMQPdebug:
                print(datetime.datetime.now().strftime('%H:%M:%S.%f') +
                ' ' + self.name + " Received \t%r" % body)

        msg = json.loads(body)

        if msg['PassCtrl'] == True:
            msg['PassCtrl'] = False
            ch.stop_consuming() # required in callback to prevent infinite loop

    def receive(self,msgQueue, callbackF):
        """Waits for msg to arrive in msgQueue, usues callbackF"""
        cParams = pika.ConnectionParameters(host=self.host)
        connection = pika.BlockingConnection(cParams)
        channel = connection.channel()

        channel.queue_declare(queue=msgQueue) # ensure queue created
        channel.basic_consume(callbackF, queue=msgQueue, no_ack=True)
        channel.start_consuming()
        # will only be reached once channel stops consuming (assumed in callback)
        connection.close()

    def redirect(self, ch, method, properties, body):
        """Method to send messages to appropriate outside functions"""
        msg = json.loads(body)
        if self.mirror:
            if self.mirror.AMQPdebug:
                print('In %s redirect...' % self.name)
                print(msg)
        msgType = msg['msgType']

        if msgType == 'init':
            ltd.amqp.IPY_init(msg)
            ch.stop_consuming()
            return

        elif msgType == 'mirrorOk':
            ltd.amqp.PY3importMir(msg)
            ch.stop_consuming()
            return

        elif msgType == 'AgentUpdate':
            ltd.amqp.agentUpdate(self.mirror, msg)

        elif msgType == 'Handoff':
            valueMatch = ltd.amqp.handoff(self.mirror, msg)
            if valueMatch:
                ch.stop_consuming()
            else:
                print('Value error...')
            return

        elif msgType == 'endSim':
            ltd.amqp.endSim(self.mirror)
            ch.stop_consuming()
            return

        # for continued debug work
        else:
            print('no matching msg type... Stoping Consume Loop')
            ch.stop_consuming()
        