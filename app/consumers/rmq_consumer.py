import pika
from config import settings


class RMQConsumer:
    def __init__(self, queue_name):
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

    def consume(self, callback):
        print(
            f"Consuming messages from '{self.queue_name}' queue. To exit press CTRL+C."
        )
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=False
        )
        self.channel.start_consuming()
