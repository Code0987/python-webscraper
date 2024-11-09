from config import settings
from .rmq_producer import RMQProducer
from ..schemas.scape_request import ScrapeRequest


def push_scrape_request(scrape_request: ScrapeRequest) -> None:
    '''
    This function is used to push scrape requests to the scrapper queue.
    The scrapper queue is a RabbitMQ queue that is used to distribute scrape requests among multiple workers.
    The workers are responsible for scraping the requested pages and storing the scraped data in the database.

    Input:
        scrape_request: A ScrapeRequest object containing the details of the scrape request.
    Output:
        None
    '''
    with RMQProducer(queue_name=settings.AMQP_SCRAPPER_QUEUE) as producer:
        producer.channel.basic_publish(
            exchange="",
            routing_key=settings.AMQP_SCRAPPER_QUEUE,
            body=scrape_request.json(),
        )
