import json

import pika


class Producer:

    def __init__(self, host: str, port: int, vhost: str, queue: str, exchange: str, routing_key: str, credentials: dict):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = None
        self.channel = None

        self.credentials = pika.PlainCredentials(**credentials)

    def init_connection(self):
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.vhost, credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def post_message(self, body, queue=None, exchange=None, routing_key=None):

        if isinstance(body, dict):
            body = json.dumps(body)

        if not queue:
            queue = self.queue

        if not exchange:
            exchange = self.exchange

        if not routing_key:
            routing_key = self.routing_key

        """
        if not self.channel:
            try:
                self.init_connection()
            except:
                raise Exception("Connection can not be establish.")
        """

        self.channel.queue_bind(queue=queue, exchange=exchange)
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
        self.channel.close()
