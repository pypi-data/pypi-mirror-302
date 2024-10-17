import json
import pika.exceptions
from .consumer import Consumer
from .producer import Producer


class AbstractAgent:

    def __init__(self, *args, **kwargs):

        # Consumer queue data
        self.consumer = Consumer(*args, **kwargs)
        try:
            self.consumer.init_connection()
        except pika.exceptions.AMQPConnectionError:
            print("No se pudo establecer la conexión con el servidor")
            exit()

    def name(self):
        return self.__class__.__name__

    def __get_methods__(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

    @staticmethod
    def __update_status__(status):
        #print(settings.STATUS[status])
        pass

    def check_access(self, data):
        print(f'Agent {self.name()} is running and you have access to him.')

    def start(self):
        self.__update_status__("Listening")
        self.consumer.start_consuming(callback=self.callback)

    def callback(self, ch, method, properties, body):
        incomming_data = json.loads(body)

        # Get what action is requested based on class's functions
        action = incomming_data.pop('action', None)

        if action and action in self.__get_methods__():

            # Do something based on action requested
            self.__update_status__('Busy')

            # Process incoming data
            try:
                data = getattr(self, action)(incomming_data['data'])
            except NotImplementedError:
                data = None
                self.__update_status__('ErrorOnRequest')

            # Getting host attributes for reply data
            reply_to = incomming_data.get('reply_to', None)

            # Send data to the appropriate queue
            if data and reply_to:
                try:
                    action = reply_to.get('action', None)
                    reply_to = reply_to['reply_to_host']
                    reply_to.update({'vhost': '/', 'port': 5672})

                    result = {
                        'action': action,
                        'reply_to': reply_to,
                        'data': data
                    }

                    self.reply_to(result)
                except KeyError:
                    self.__update_status__('ErrorOnResponse')

            self.__update_status__('Listening')
        else:
            print("Not provided action")

    def reply_to(self, body):
        reply_to = body.pop('reply_to')
        print(reply_to['credentials'])

        # Instancing new Producer for send reply data
        producer = Producer(
            host=reply_to['host'],
            vhost=reply_to['vhost'],
            port=reply_to['port'],
            queue=reply_to['queue'],
            exchange=reply_to['exchange'],
            routing_key=reply_to['routing_key'],
            credentials=reply_to['credentials']
        )
        producer.init_connection()
        producer.post_message(body=json.dumps(body))

        self.__update_status__('SuccessOnResponse')
