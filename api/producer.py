import pika


class Producer:
    channel = None

    def connect(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('localhost'))

            self.channel = connection.channel()
        except pika.exceptions.AMQPConnectionError:
            print("ERROR CONNECTION TO RABBITMQ")

    def handleLog(self, message: str):
        try:
            if self.channel is None or not self.channel.is_open:
                self.connect()

            self.channel.exchange_declare(
                exchange="logs", exchange_type="direct", durable=True)

            print("sending message: {}".format(message))

            self.channel.basic_publish(exchange='logs',
                                       routing_key='',
                                       body=message,
                                       properties=pika.BasicProperties(
                                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                       ))
        except pika.exceptions.ConnectionClosed:
            print("Connection closed. Trying to reconnect")
            self.connect()
            self.handleLog(message)
        except pika.exceptions.ConnectionClosedByBroker:
            print(">>> Connection was closed by the broker")
            raise Exception(
                "BrokerError", "Could not deliver the message to the broker")
        except pika.exceptions.ChannelWrongStateError:
            print("ChannelError", "Failed to use the channel")
            raise Exception("ChannelError", "Failed to use the channel")
        except pika.exceptions.StreamLostError:
            print("Stream EOF Error", "Stream has ended")
            raise Exception("ChannelError", "Failed to use the channel")
        except AttributeError:
            raise Exception("ReconnectError", "Could not reconnect")
