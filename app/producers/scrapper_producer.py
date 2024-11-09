from config import settings
from .rmq_producer import RMQProducer
from ..schemas.scape_request import ScrapeRequest


def push_scrape_request(scrape_request: ScrapeRequest):
    with RMQProducer(queue_name=settings.AMQP_SCRAPPER_QUEUE) as producer:
        producer.channel.basic_publish(
            exchange="",
            routing_key=settings.AMQP_SCRAPPER_QUEUE,
            body=scrape_request.json(),
        )
