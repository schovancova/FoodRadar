import threading

from requests_html import HTMLSession
from sqlalchemy.orm import sessionmaker

from src.modules.connector import engine
from src.modules.product import ProductTesco
from src.modules.store import Tesco
from src.modules.logger import get_logger


def stop_scraping():
    my_threads = threading.enumerate()
    while any(isinstance(thread, Scraper) for thread in my_threads):
        for thread in my_threads:
            if isinstance(thread, Scraper):
                thread.stop()
        my_threads = threading.enumerate()


class Scraper(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = kwargs['target']
        self._stop_event = threading.Event()
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(Scraper, self).join(*args, **kwargs)

    def run(self):
        logger = get_logger()
        logger.info(f"Starting a scraper {threading.get_ident()}")
        store = Tesco(self.category.store)
        page = 1
        html_session = HTMLSession()
        while not self._stop_event.is_set():
            request = html_session.get(store.get_category_link(self.category.link) + str(page))
            products = request.html.xpath(store.xpath["products"])
            if not products:
                break
            for p in products:
                if self._stop_event.is_set():
                    break
                product = ProductTesco(self.session, self.category.store.id, p)
                product_link = product.get_link(store.products_link)
                request = html_session.get(product_link)
                nutrients_div = request.html.xpath(product.xpath["nutrients_div"], first=True)
                if not nutrients_div:
                    continue
                calories = product.get_calories(nutrients_div)
                if not calories:
                    logger.error(f"No calories found for {p.text} {product_link}")
                price_div = request.html.xpath(product.xpath["price_div"], first=True)
                price = product.get_price(price_div)
                product_info = dict(
                    name=p.text,
                    calories=calories,
                    price=price,
                    unit_price=True,
                    unit_type="kg",
                    category_id=self.category.id,
                    store_product_id=product.product_id,
                    store_id=store.store.id)
                product.update_or_insert(**product_info)
            page += 1
        logger.info(f"Stopping a scraper {threading.get_ident()}")
        self.session.commit()

