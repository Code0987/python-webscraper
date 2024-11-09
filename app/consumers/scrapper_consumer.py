import json
from config import settings
from .rmq_consumer import RMQConsumer
from ..services.scrappers.dentalstall_products_scrapper import (
    DentalStallProductsScraper,
)
from ..services.storage.files_storage import FilesStorage
from ..services.notifications.print_notifier import PrintNotifier
from ..schemas.scape_request import ScrapeRequest
from ..db import products_db


notifier = PrintNotifier()


def callback(channel, method, properties, body):
    scrape_request: ScrapeRequest = ScrapeRequest(**json.loads(body))
    print(f"Received scrape request: {scrape_request}")

    try:
        # Scrape all products from website as per request
        scraper = DentalStallProductsScraper(
            page_limit=scrape_request.page_limit,
            proxy_url=scrape_request.proxy_url,
        )
        products = scraper.scrape()

        n_products_scraped = len(products)
        n_products_updated = 0

        # Update products in database if price has changed
        for product in products:
            existing_product = products_db.get(
                key_name="title", key_value=product.title
            )
            if not existing_product or existing_product["price"] != product.price:
                products_db.put(
                    key_name="title", key_value=product.title, data=product.dict()
                )
                n_products_updated += 1

        # Notify scrape completion
        notifier.notify(
            f"Scraped {n_products_scraped} products. Updated {n_products_updated} products."
        )
    except Exception as e:
        print(f"Error while scraping: {e}")

        # Notify scrape failure
        notifier.notify(f"Scraping failed: {e}")

    # Acknowledge message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    with RMQConsumer(queue_name=settings.AMQP_SCRAPPER_QUEUE) as consumer:
        consumer.consume(callback)
