import pika
from config import settings


class RMQProducer:
    def __init__(self, queue_name: str):
        self.connection = None
        self.channel = None
        self.queue_name = queue_name

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(settings.AMQP_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.channel and self.channel.is_open:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
