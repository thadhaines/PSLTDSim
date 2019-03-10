import json
import pika
import datetime

class AMQPAgent():
    """Can send and receive msgs, init with host string and msg format
        uses json dumps and loads to send/receive native python objects"""
    def __init__(self, name, host, msg=None):
        self.name = name
        self.host = host
        self.msg = msg

    def send(self,msgQueue,msg):
        """send msg to msgQueue"""
        cParams = pika.ConnectionParameters(host=self.host)
        connection = pika.BlockingConnection(cParams)
        channel = connection.channel()

        channel.queue_declare(queue=msgQueue) # ensure queue created
        print(datetime.datetime.now().strftime('%H:%M:%S.%f') +
            ' ' + self.name + " Sending \t %r" % json.dumps(msg))
        channel.basic_publish(exchange='', 
                              routing_key=msgQueue, 
                              body=json.dumps(msg) )
        connection.close()

    def callback(self, ch, method, properties, body):
        """should be altered to specific needs - proof of concept shown"""
        print(datetime.datetime.now().strftime('%H:%M:%S.%f') +
            ' ' + self.name + " Received \t%r" % body)

        self.msg = json.loads(body)

        if self.msg['PassCtrl'] == True:
            self.msg['PassCtrl'] = False
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
        