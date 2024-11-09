import json
from typing import Optional
import httpx
from bs4 import BeautifulSoup
import re
from time import sleep
from urllib.parse import quote

from .products_scrapper import ProductsScrapper
from app.db.models.product import Product
from app.db import files_db, cache_db


SCRAPE_URL_FORMAT = "https://dentalstall.com/shop/page/{page}/"


class DentalStallProductsScraper(ProductsScrapper):
    '''
    This class is a subclass of the ProductsScrapper class and is responsible for scraping products from the DentalStall website product pages defined by `https://dentalstall.com/shop/page/{page}/`.
    It uses the ProductsScrapper class to scrape the products and then processes the scraped data to extract the necessary information.
    It also caches the scraped data in Redis to avoid scraping the same products multiple times.
    '''

    def __init__(
        self,
        page_limit: int = 5,
        proxy_url: str = None,
        http_retry_count: int = 3,
        http_retry_interval: int = 30,
    ):
        self.page_limit = page_limit
        self.proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else {}
        self.http_retry_count = http_retry_count
        self.http_retry_interval = http_retry_interval

    def __parse_title(self, element: any) -> float:
        value = element.text if element is not None else ""
        return value.strip()

    def __parse_price(self, element: any) -> float:
        # Regex to convert price with symbols to just numeric value
        price = element.text if element is not None else "0"
        value = re.sub(r"[^\d.]", "", price)
        value = float(value)
        return value

    def __process_image(self, element: any) -> Optional[str]:
        # Download image to DB (folder in this case)
        # Return DB key (path in this case) of image
        key = None
        try:
            image_url = element.get("data-lazy-src", element.get("src"))
            resp = httpx.get(image_url, proxies=self.proxies)
            key = quote(image_url, "")
            files_db.put(key, resp.content)
        except Exception as e:
            print("Unable to download image", e)
        return key

    def parse_page(self, page_html_content: str) -> list["Product"]:
        '''
        This function parses the HTML content of pages (with url as `SCRAPE_URL_FORMAT`) and extracts the products from it.
        It returns a list of `Product` objects representing the products found on the page.
        It also caches the products in Redis, to avoid scraping the same products multiple times.

        Input:
            page_html_content: The HTML content of a single page.
        Output:
            A list of Product objects representing the products found on the page.
        '''
        soup = BeautifulSoup(page_html_content, "html.parser")
        products = []
        for element in soup.select("#mf-shop-content .products .product-inner"):
            title = self.__parse_title(element.select_one(".woo-loop-product__title"))
            if not title:
                print(f"Product title not found: {element}")
                continue

            price = self.__parse_price(element.select_one(".woocommerce-Price-amount"))
            if not price:
                print(f"Product price not found: {element}")
                continue
        
            # Check in cache if product's price has changed
            existing_product = cache_db.get(key=f"product_{title}")
            if existing_product and json.loads(existing_product).get("price", float('inf')) == price:
                continue
            print(f"Price changed or does not exist for product in cache: {title}")

            image_path = self.__process_image(
                element.select_one(".attachment-woocommerce_thumbnail")
            )
            if not image_path:
                print(f"Product image not found: {element}")
                continue

            product = Product(
                title=title,
                price=price,
                image_path=image_path,
            )
            
            # Cache product in Redis
            cache_db.put(key=f"product_{product.title}", data=json.dumps(product.dict()))

            products.append(product)
            print(f"Found product with title: {product.title}")
        return products

    def scrape(self) -> list["Product"]:
        '''
        This function scrapes all pages (upto `page_limit`) and returns a list of `Product` objects representing the products found.

        Input:
            None
        Output:
            A list of Product objects representing the products found.
        '''
        products = []
        with httpx.Client(proxies=self.proxies, follow_redirects=True) as client:
            for page in range(1, self.page_limit + 1):
                print(f"Scraping page {page}")
                try_count = 0
                while try_count < self.http_retry_count:
                    try:
                        resp = client.get(SCRAPE_URL_FORMAT.format(page=page))
                        resp.raise_for_status()

                        products.extend(self.parse_page(resp.text))
                    except httpx.HTTPStatusError as e:
                        print(f"Failed to retrieve page {page}: {e}")
                        sleep(self.http_retry_interval)
                        print(f"Retrying page {page}")
                    try_count += 1
        return products
