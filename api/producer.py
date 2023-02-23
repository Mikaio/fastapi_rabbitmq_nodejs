import pika

class Producer:
    channel = None
    
    def connect(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

        self.channel = connection.channel()
    
    def handleLog(self, message: str):
        if not self.channel:
            self.connect()

        self.channel.exchange_declare(exchange="logs", exchange_type="direct", durable=True)

        self.channel.basic_publish(exchange='logs',
                                    routing_key='',
                                    body=message,
                                    properties=pika.BasicProperties(
                                        delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                                        ))