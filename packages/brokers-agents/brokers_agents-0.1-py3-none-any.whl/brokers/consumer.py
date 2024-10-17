import pika


class Consumer:

    def __init__(self, host=None, port=None, vhost=None, queue=None, exchange=None, routing_key=None, credentials=None):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key

        self.connection = None
        self.channel = None
        self.listening = False

        self.credentials = pika.PlainCredentials(**credentials)

    def init_connection(self):
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost, credentials=self.credentials, heartbeat=10)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()
        self.listening = True

    def start_consuming(self, callback, queue=None):
        if not self.listening:
            self.init_connection()

        if not queue:
            queue = self.queue

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
