from src.modules.connector import session, Store, Category
from src.cron.scrape_category import scrape


# TODO change to fetchall when more stores come up
actual_store = session.query(Store).first()
categories = session.query(Category).filter(Category.store == actual_store.id).all()

for category in categories:
    scrape(actual_store, category)
